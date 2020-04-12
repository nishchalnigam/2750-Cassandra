# 2750-Cassandra

## Part 1: Installing Cassandra on the linux VM's

1. Make sure JAVA_HOME path is added in the "~/.bashrc" file
  Type `sudo vim ~/.bashrc` and add the path in the end. The path is usually in the `/usr/lib/jvm/` folder.

  ![alt text](https://github.com/nishchalnigam/2750-Cassandra/blob/master/Gallery/Bashrc%20file.JPG) 
  
  Check the Path by typing `echo JAVA_HOME`

2. Make sure "curl" is installed, else install it using apt-get

3. To install Cassandra on your node, type the following commands, or Follow these instructions: http://cassandra.apache.org/download/:

  `echo "deb https://downloads.apache.org/cassandra/debian 311x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list`

  Add the Apache Cassandra repository keys:
  `curl https://downloads.apache.org/cassandra/KEYS | sudo apt-key add -`

  Update the repositories:
  `sudo apt-get update`

  Install Cassandra:
  `sudo apt-get install cassandra`
