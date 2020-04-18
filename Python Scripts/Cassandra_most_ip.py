from cassandra.cluster import Cluster

cluster = Cluster(['206.81.9.191','67.205.176.120','206.81.9.184'])

session = cluster.connect('cloud_log')


rows = session.execute("select count(ip_address) as ip_count, ip_address from access_log group by ip_address;")

max_count = 0
max_ip = ''

for row in rows:
    if row.ip_count > max_count:
        max_count = row.ip_count
        max_ip = row.ip_address
        
	
print "IP: ", max_ip, " has been accessed ", max_count, " times"
