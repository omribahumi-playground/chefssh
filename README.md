#chefssh#

##Preface##
We've been using [AWS][1] [EC2][2] for a while now, using [Opscode Chef][3] as our inventory/configuration management. The thing is, if you're not using static IP addresses for your chef nodes (non elastic IPs on EC2), tracking the nodes IP addresses is a whole lot of hassle. Furthermore, if you happen to have more than one node of each kind, starting to keep distinct DNS records for each is simply not fun.

If you're like me, you're using [knife][4] for tracking your inventory and querying for nodes' IP addresses. The thing is, if you want to transfer a file to a machine using scp, you'll probably have to run one or two knife commands, then executing SCP to transfer files to/from it. Most of the people write a script to make this easier, however, you'll probably loose some scp functionality (i.e. adding arguments to the scp command line)

This is the exact reason I created chef-ssh and chef-scp for. Making a user-friendly ssh and scp commands for chef.

##Requirements##
To use this tool, you'll need a `knife.rb` in your `~/.chef` folder (this is actually a requirement for using `knife` in general). Install this with `sudo pip install git+git://github.com/omribahumi/chefssh.git`

Note for Ubuntu users: because this tool uses [PyChef][5] for interfacing chef server, you might get a Python exception complaining about it not being able to load `libcrypto.so`, simply run `sudo apt-get install libssl-dev` to solve this.

##Usage##
Using the `chef-ssh` and `chef-scp` commands is as simple as using the `ssh` and `scp` commands. The format is the same, only that hostnames are being treated differently. When these command encounter a hostname, they perform a chef node search on various attributes, trying to match `*hostname*`. If more than one node matches, it prompts the user to select one.

For example, lets say you have a node named `webserver` in chef and you'd like to SCP a file to it, instead of doing a `knife node show webserver` and retrieving the IP address, then invoking `scp /path/to/file <ipaddress>:`, you'd simply run `chef-scp /path/to/file webserver:` !

The case for `chef-ssh` is pretty similar, say you'd like to ssh to `webserver`, you'd simply run `chef-ssh webserver`.

##Why use this script instead of regular knife ssh##
* Saving you time typing the node search query
* User-friendly. No need to be familiar with the solr search syntax
* Sometimes, you just want to SSH a single node matching the query, not all of them
* Letting you pass command line arguments to the underlying SSH/SCP commands
* Doesn't require chef installation on the machine, only pychef

[1]: http://aws.amazon.com/
[2]: http://aws.amazon.com/ec2/
[3]: http://www.opscode.com/chef/
[4]: http://docs.opscode.com/knife.html
[5]: http://pychef.readthedocs.org/
