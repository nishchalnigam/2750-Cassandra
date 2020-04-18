from cassandra.cluster import Cluster

cluster = Cluster(['206.81.9.191','67.205.176.120','206.81.9.184'])

session = cluster.connect('cloud_log')


rows = session.execute("select count(path) as path_count, path from request_line_details  group by path;")

max_count = 0
max_path = ''

for row in rows:
    if row.path_count > max_count:
        max_count = row.path_count
        max_path = row.path


print "Path: ", max_path, " has been hit ", max_count, " times"

