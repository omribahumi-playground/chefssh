import commandbase

class ScpArgument(object):
    """
        Parse and split SCP argument string

        Possible formats:
            '/path/to/file' - local file/folder reference
            'remote:/path/to/file' - remote file/folder reference, without username
            'username@remote:/path/to/file' - remote file/folder reference with username
            'remote:' - remote without path and username, references home directory on remote
            'username@remote:' - remote without path but with username, reference home directory on remote
        i.e.:
            'root@127.0.0.1:/etc' will be parsed to object.username = 'root',
                                                    object.hostname = '127.0.0.1',
                                                    object.path = '/etc'
            '/boo' will be parsed to object.username = '',
                                     object.hostname = '',
                                     object.path = '/boo'
    """
    def __init__(self, arg):
        self.username, self.hostname, self.path = None, None, None

        if ':' in arg:
            # remote path
            hostname, self.path = arg.split(':', 1)
            if '@' in hostname:
                self.username, self.hostname = hostname.split('@', 1)
            else:
                self.hostname = hostname
        else:
            # local path
            self.path = arg

    def isLocal(self):
        return not bool(self.hostname)

    def isRemote(self):
        return bool(self.hostname)

    def __str__(self):
        ret = ''
        if self.username:
            ret += self.username + '@'
        if self.hostname:
            ret += self.hostname + ':'
        ret += self.path

        return ret

    def __repr__(self):
        return '<%s username=%r hostname=%r path=%r>' % (self.__class__.__name__,
                                                         self.username, self.hostname)

class ScpCommand(commandbase.ChefCommand):
    def __init__(self):
        super(ScpCommand, self).__init__('scp', 2)

    def getUsage(self, command_name):
        return "\n".join(
                ['usage: %s [scp_arguments] <source> <dest>' % (command_name,),
                 '       if source and/or dest are non-local, a chef node search is performed',
                 '       the hostname portion of the path is searched in the following node attributes:',
                 '          hostname, instance id, private ip, public ip'])

    def parseAndSearch(self, argument, api):
        scp_argument = ScpArgument(argument)
        if scp_argument.isRemote():
            scp_argument.node = self.search(scp_argument.hostname, api)
            scp_argument.hostname = self.getNodeIpAddress(scp_argument.node)
        return scp_argument

