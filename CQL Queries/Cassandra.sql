CREATE KEYSPACE test_keyspace WITH replication = {'class': 'SimpleStrategy','replication_factor':'1'} AND durable_writes = 'true';

use cloud_log ;

DROP table access_log;

CREATE TABLE access_log (IP_Address text, client_id text, client_username text, time text,timezone text, request_line text, status_code text, object_size text, PRIMARY KEY(IP_Address,time,request_line));

COPY access_log (IP_Address , client_id , client_username , time , timezone , request_line , status_code, object_size) FROM '/home/student/access_log' WITH DELIMITER=' ';

select * from access_log where IP_Address = '10.207.188.188' limit 5;


--How many hits were made from the IP: 10.207.188.188? 
select count(*) from cloud_log.access_log where IP_Address = '10.207.188.188' ;