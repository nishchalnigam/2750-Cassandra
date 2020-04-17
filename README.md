# Multi-Node Cluster Database with Cassandra on Linux

## Part 1: Setting up Cassandra on the Linux VM's
### A: Setup on Individual Nodes

1. Make sure JAVA_HOME path is added in the "~/.bashrc" file  
	Type `sudo vim ~/.bashrc` and add the path in the end. The path is usually in the `/usr/lib/jvm/` folder.

	![alt text](https://github.com/nishchalnigam/2750-Cassandra/blob/master/Gallery/Bashrc%20file.PNG) 
  
	Check the Path by typing `echo $JAVA_HOME`

2. Make sure **curl** is installed, else install it using apt-get

3. To install Cassandra on your node, type the following commands, or Follow these instructions: http://cassandra.apache.org/download/:

	`echo "deb https://downloads.apache.org/cassandra/debian 311x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list`

	Add the Apache Cassandra repository keys:
	
	`curl https://downloads.apache.org/cassandra/KEYS | sudo apt-key add -`

	Update the repositories:
	
	`sudo apt-get update`

	Install Cassandra:
	
	`sudo apt-get install cassandra`

4. Start Cassandra with `sudo service cassandra start` and check the status using `nodetool status` and `sudo service cassandra status` commands:

	![alt text](https://github.com/nishchalnigam/2750-Cassandra/blob/master/Gallery/Nodetool%20status.JPG) 

### B: Configure Cassandra nodes to make them work together

1. Stop Cassandra on all three nodes:  
	`sudo service cassandra stop`

2. Delete the default dataset:  
	`sudo rm -rf /var/lib/cassandra/data/system/*`

3. Edit the configuration file **cassandra.yaml** on all 3 nodes.It is located in the /etc/cassandra directory:

	a. The directive `cluster_name` should be same across all the nodes:  
	`cluster_name: 'Test Cluster'`
	
	b. Update `-seeds:` by adding all 3 IP addresses, separated by commas:  
	`seeds: "206.81.9.191,67.205.176.120,206.81.9.184"`
	
	c. Update `listen_address` and `rpc_address` on each node to the IP address to that node.  
	For "206.81.9.191", it should look like:  
	`listen_address: 206.81.9.191`  
	`rpc_address: 206.81.9.191`
	
	d. Update `endpoint_switch` from `SimpleSnitch` to `GossipingPropertyFileSnitch`:  
	`endpoint_snitch: GossipingPropertyFileSnitch`
	
	e. Finally, add the following directive at the end of the file:  
	`auto_bootstrap: false`
	
	Save the **cassandra.yaml** file all on 3 nodes

4. Start Cassandra on all 3 nodes again:  
	`sudo service cassandra start`

5. Check the status of the clusters with the `sudo nodetool status` command. All 3 nodes should be listed:  

	![alt text](https://github.com/nishchalnigam/2750-Cassandra/blob/master/Gallery/MutliNodeCluster.PNG) 


## Part 2: Importing Data into Cassandra:

1. Make sure Python is installed on the VM, and then run CQL with the `cqlsh <nodeIPAdress>` command.  

2. In the CQL Terminal, create a keyspace:  
	`CREATE KEYSPACE cloud_log WITH replication = {'class': 'SimpleStrategy','replication_factor':'1'} AND durable_writes = 'true';`
	
	Use that keyspace with the `use cloud_log ;` command.

3. Create a table in the **cloud_log** keyspace with all the **Common Log Format** columns :  

	`CREATE TABLE access_log (IP_Address text, client_id text, client_username text, time text,timezone text, request_line text, status_code text, object_size text, PRIMARY KEY(IP_Address,time,request_line));`
	
	Here, we are using the combination of IP_Address, timestamp and request line as the primary key.
	
4. Import the access_log data into your table using the copy command:

	`COPY access_log (IP_Address , client_id , client_username , time , timezone , request_line , status_code, object_size) FROM '/home/student/access_log' WITH DELIMITER=' ';`

	Check the data with a simple select query:  
	`select * from access_log where IP_Address = '10.207.188.188' limit 5;`
	
	![alt text](https://github.com/nishchalnigam/2750-Cassandra/blob/master/Gallery/ImportingAccessLog.png) 

## Create additional table `Request_line_details` to operate on `path` in the `request_line` column:  

1. In order to run CQL Queries on `path`, we need to make another table with `path` as the main primary key.
	`CREATE TABLE Request_line_details (IP_Address text, time text,method text, path text, protocol text, PRIMARY KEY(path,IP_Address,time,method,protocol));`

2. To load data into this table, we first need to split the `request_line` column. In order to do so, we first export the data into a new csv file:  
	`COPY cloud_log.access_log (ip_address,time,request_line) TO 'requestline.csv' with DELIMITER = ' ' and QUOTE = ' ';`

3. Next, we copy data from **requestline.csv** to the `request_line_details` table:  
	`COPY cloud_log.request_line_details  (IP_ADDRESS,time,method, path, protocol) FROM 'requestline.csv' WITH DELIMITER = ' ' and QUOTE = '"' and ESCAPE = '*';`
	
	Check the data with a simple select query:
	`select * from request_line_details limit 5;`
	![alt text](https://github.com/nishchalnigam/2750-Cassandra/blob/master/Gallery/Request_line.PNG) 


## Part 3: Operate Data in Cassandra:

1. How many hits were made to the website item “/assets/img/release-schedule-logo.png”?  
	Ans: 24292
	
	`select count(*) from request_line_details where path = '/assets/img/release-schedule-logo.png\';`
	![alt text](https://github.com/nishchalnigam/2750-Cassandra/blob/master/Gallery/Q1.PNG)

2. How many hits were made from the IP: 10.207.188.188?
	Ans: 398

	`select count(*) from cloud_log.access_log where IP_Address = '10.207.188.188' ;`
	![alt text](https://github.com/nishchalnigam/2750-Cassandra/blob/master/Gallery/Q2.PNG) 


3. Which path in the website has been hit most? How many hits were made to
the path?

4. Which IP accesses the website most? How many accesses were made by it?
 


