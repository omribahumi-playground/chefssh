import abc
import exceptions
import subprocess
import re
import getopt
import chef
import os
from chef.fabric import DEFAULT_HOSTNAME_ATTR

def search_pick_node(search_query, api):
    """
        Perform node search for `search_query` with `api`,
        lets the user pick interactivly if there are multiple nodes returned
        Throws LookupError if can't find a matching node
    """
    nodes = [node for node in chef.Search('node', search_query, api=api)]
    node = None

    # no nodes match the search
    if not nodes:
        raise exceptions.LookupError("Can't find a node matching %s" % (search_query,))
    # more than one node matched the search. let the user choose one
    elif len(nodes) > 1:
        # sort the results before displaying them
        nodes.sort(lambda a,b: cmp(a.object.name.lower(), b.object.name.lower()))

        print '%d nodes matched your query:' % (len(nodes),)
        for i, current_node in enumerate(nodes):
            print "\t%d. %s" % (i+1, current_node.object.name,)

        while not node:
            selected_node = raw_input('Please select one: ')
            if not selected_node.isdigit() or not 1 <= int(selected_node) <= len(nodes):
                print 'Invalid selection. Please choose a number between 1 and %d' % (len(nodes),)
            else:
                node = nodes[int(selected_node) - 1]
                print
    # only one result. that's our node.
    else:
        node = nodes[0]

    return node

def command_getopt(command):
    """
        Executes `command` and parses the usage output, generating a getopt()
        format for parsing those arguments.

        Known issues:
            * Only supports short options
            * Some commands (like ping on OSX) have two operation modes.
              It doesn't parse those correctly.
    """
    process = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    usage = process.communicate()[0]
    process.wait()

    parsed_usage = re.findall(r'(?<=\[\-)[^\s\]]+', usage)

    # first match is arguments without parameters, the rest are parameterized
    # format them correctly
    if len(parsed_usage) > 1:
        parsed_usage = [parsed_usage[0], ":".join(parsed_usage[1:])]

    return "".join(parsed_usage)

class ChefCommand(object):
    """
        Base class for implementing chef commands
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, command, argument_count):
        self.command = command
        self.argument_count = argument_count
        self.getopt_options = command_getopt(self.command)
        self.node_search_attributes = ['hostname', 'fqdn', 'ipaddress', 'ec2_local_ipv4',
                                       'ec2_public_ipv4', 'ec2_instance_id',
                                       'ec2_public_hostname', 'ec2_local_hostname', 'name']

    def getNodeIpAddress(self, node):
        """
            Return the IP address of the node object `node`
        """
        for attribute in DEFAULT_HOSTNAME_ATTR:
            try:
                return node.object.attributes.get_dotted(attribute)
            except KeyError:
                continue
        else:
            return None

    def search(self, string, api):
        """
            Search attributes `self.node_search_attributes` to find `string` using `api`
            Returning a chef node object
            If multiple nodes are matched, lets the user pick interactivly
        """
        node_search_query = ' OR '.join(
            ['%s:*%s*' % (attribute, string) for attribute in self.node_search_attributes])
        node = search_pick_node(node_search_query, api)

        return node

    def invoke(self, extra_args, arguments):
        command_args = [self.command] + extra_args + [str(argument) for argument in arguments]

        print 'Invoking %s' % (" ".join(command_args))
        os.execvp(command_args[0], command_args)

    @abc.abstractmethod
    def getUsage(self, command_name):
        pass

