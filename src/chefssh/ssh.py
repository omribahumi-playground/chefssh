import commandbase

class SshArgument(object):
    """
        Parse and split SSH argument string.

        Possible formats:
            '127.0.0.1' - hostname without username
            'user@127.0.0.1' - hostname with username
        i.e.:
            root@127.0.0.1 will be parsed to object.username = 'root',
                                             object.hostname = '127.0.0.1'
            127.0.0.1 will be parsed to object.username = '',
                                        object.hostname = '127.0.0.1'
    """

    def __init__(self, arg):
        self.username, self.hostname = None, None
        if '@' in arg:
            self.username, self.hostname = arg.split("@", 1)
        else:
            self.hostname = arg

    def __str__(self):
        if self.username:
            return '%s@%s' % (self.username, self.hostname)
        else:
            return self.hostname

    def __repr__(self):
        return '<%s username=%r hostname=%r>' % (self.__class__.__name__,
                                                self.username, self.hostname)

class SshCommand(commandbase.ChefCommand):
    def __init__(self):
        super(SshCommand, self).__init__('ssh', 1)

    def getUsage(self, command_name):
        return "\n".join(
                ['usage: %s [ssh_arguments] <node>' % (command_name,),
                 '       node can be hostname/instance id/private ip/public ip'])

    def parseAndSearch(self, argument, api):
        ssh_argument = SshArgument(argument)
        ssh_argument.node = self.search(ssh_argument.hostname, api)
        ssh_argument.hostname = self.getNodeIpAddress(ssh_argument.node)
        return ssh_argument

