# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.define "alpha" do |alpha|
      alpha.vm.box = "ubuntu/xenial64"
      # set up network ip and port forwarding
      alpha.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"
      alpha.vm.network "private_network", ip: "192.168.33.10"

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

  if File.exists?(File.expand_path("~/.gitconfig"))
    config.vm.provision "file", source: "~/.gitconfig", destination: "~/.gitconfig"
  end

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
  SHELL

  # set enviroment varaibles
  config.vm.provision "shell", privileged: false, inline: <<-SHELL
  cat<< 'EOF' >> ~/.profile
export DB_USERNAME=root
export DB_PASSWORD=passw0rd
export DB_HOST=localhost
export DB_PORT=3306
export DB_DBNAME=development
EOF
  
  source ~/.profile
  cd /vagrant
  python db_create.py

  # Install PhantomJS for Selenium browser support
  echo "\n***********************************"
  echo " Installing PhantomJS for Selenium"
  echo "***********************************\n"
  sudo apt-get install -y chrpath libssl-dev libxft-dev
  # PhantomJS https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
  cd ~
  export PHANTOM_JS="phantomjs-2.1.1-linux-x86_64"
  wget https://bitbucket.org/ariya/phantomjs/downloads/$PHANTOM_JS.tar.bz2
  sudo tar xvjf $PHANTOM_JS.tar.bz2
  sudo mv $PHANTOM_JS /usr/local/share
  sudo ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/bin
  rm -f $PHANTOM_JS.tar.bz2

  SHELL

end
