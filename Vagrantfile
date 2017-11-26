# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.define "alpha" do |alpha|
      alpha.vm.box = "ubuntu/xenial64"
      # set up network ip and port forwarding
      alpha.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"
      alpha.vm.network "private_network", ip: "192.168.33.10"

      # Windows users need to change the permissions explicitly so that Windows doesn't
      # set the execute bit on all of your files which messes with GitHub users on Mac and Linux
      alpha.vm.synced_folder "./", "/vagrant", owner: "ubuntu", mount_options: ["dmode=755,fmode=644"]

      alpha.vm.provider "virtualbox" do |vb|
        # Customize the amount of memory on the VM:
        vb.memory = "512"
        vb.cpus = 1
        vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
        vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
      end
  end

  # Add Mysql docker container
  config.vm.provision "docker" do |d|
    d.pull_images "centurylink/mysql:5.5"
    d.run "centurylink/mysql:5.5",
      args: "-d --name mysql -p 3306:3306 -v /var/lib/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=passw0rd"
  end


  # Copy your .gitconfig file so that your git credentials are correct
  if File.exists?(File.expand_path("~/.gitconfig"))
    config.vm.provision "file", source: "~/.gitconfig", destination: "~/.gitconfig"
  end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    # add cloud foundry tool
    wget -q -O - https://packages.cloudfoundry.org/debian/cli.cloudfoundry.org.key | sudo apt-key add -
    echo "deb http://packages.cloudfoundry.org/debian stable main" | sudo tee /etc/apt/sources.list.d/cloudfoundry-cli.list
    apt-get update
    apt-get install -y git cf-cli python-pip python-dev build-essential mysql-client
    pip install --upgrade pip
    apt-get -y autoremove
    # Install app dependencies
    cd /vagrant
    sudo pip install -r requirements.txt
    # Initialize database
    python db_create.py development
    python db_create.py test
    # Make vi look nice
    # sudo -H -u ubuntu echo "colorscheme desert" > ~/.vimrc
  SHELL

end
