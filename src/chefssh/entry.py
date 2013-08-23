import getopt
import sys
import chef
from ssh import SshCommand
from scp import ScpCommand

def ssh():
    run(SshCommand())

def scp():
    run(ScpCommand())

def run(command):
    flags, arguments = None, None
    try:
        flags, arguments = getopt.getopt(sys.argv[1:], command.getopt_options)
    except getopt.GetoptError:
        print command.getUsage(sys.argv[0])
        sys.exit(0)

    if len(arguments) != command.argument_count:
        print 'error: Wrong argument count'
        print command.getUsage(sys.argv[0])
        sys.exit(1)

    api = chef.autoconfigure()

    for i, argument in enumerate(arguments):
        argument = command.parseAndSearch(argument, api)
        arguments[i] = argument

    for argument in arguments:
        if getattr(argument, 'node', None):
            node = argument.node
            # print some information on the chosen node and connect to it
            print 'Node %s:' % (node['name'],)
            print '\trun_list: %s' % (', '.join(node['run_list']),)
            print '\troles: %s' % (', '.join(node['automatic']['roles']),)
            print '\trecipes: %s' % (', '.join(node['automatic']['recipes']),)
            print '\tEC2 instance type %s' % (node['automatic']['ec2']['instance_type'],)
            print

    extra_args = [item for sublist in flags for item in sublist]
    command.invoke(extra_args, arguments)

