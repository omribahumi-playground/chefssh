#chefssh#

##Preface##
I've been using [AWS][1] [EC2][2] for a while now, using [Opscode Chef][3] as my inventory/configuration management. The thing is, if you're not using static IP addresses for your chef nodes (ELB on EC2), tracking the nodes IP addresses is alot of hassle. Furthermore, if you happen to have more than one node of each kind, starting to keep distinct DNS records for each won't help you much.

If you're like me, you're using [knife][4] for tracking your inventory and querying for nodes' IP addresses. The thing is, if you want to ssh to a machine, you'll probably have to run one or two knife commands, then executing SSH. Most of the people write a script to make this easier, however, you'll probably loose some ssh functionality (i.e. adding arguments to the ssh command line)

This is the exact reason I created chef-ssh for. Making a chef friendly ssh and scp commands.

##Requirements##
To use this tool, you'll need a `knife.rb` in your `~/.chef` folder (this is actually a requirement for using `knife` in general). Install this with `sudo pip install git+git://github.com/omribahumi/chefssh.git`

Note for Ubuntu users: because this tool uses [PyChef][5] for interfacing chef server, you might get a Python exception complaining about it not being able to load `libcrypto.so`, simply run `sudo apt-get install libssl-dev` to solve this.

##Usage##
Using the `chef-ssh` and `chef-scp` commands is as simple as using the `ssh` and `scp` commands. The format is the same, only that hostnames are being treated differently.

For example, lets say you have a node named `webserver` in chef and you'd like to SSH to it, instead of doing a `knife node show webserver` and retrieving the IP address, then invoking `ssh <ipaddress>`, you'd simply run `chef-ssh webserver` !
`chef-ssh` will then perform a knife-like search on your chef server, looking for nodes matching `*webserver*` in several node attributes.
If more than one node matches the search, you'll receive an interactive prompt for choosing one.

The case for `chef-scp` is pretty similar, say you'd like to copy `/var/log/messages` from a remote server to your `/tmp` directory. Instead of running `scp ipaddress:/var/log/messages /tmp` , you'd simply run `chef-scp webserver:/var/log/messages /tmp`. `chef-scp` replaced the chef node name with the node's IP address.

[1]: http://aws.amazon.com/
[2]: http://aws.amazon.com/ec2/
[3]: http://www.opscode.com/chef/
[4]: http://docs.opscode.com/knife.html
[5]: http://pychef.readthedocs.org/
