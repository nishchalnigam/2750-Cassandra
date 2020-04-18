--Create Keyspace and import data
CREATE KEYSPACE cloud_log WITH replication = {'class': 'SimpleStrategy','replication_factor':'1'} AND durable_writes = 'true';

use cloud_log ;

DROP table access_log;

CREATE TABLE access_log (IP_Address text, client_id text, client_username text, time text,timezone text, request_line text, status_code text, object_size text, PRIMARY KEY(IP_Address,time,request_line));

COPY access_log (IP_Address , client_id , client_username , time , timezone , request_line , status_code, object_size) FROM '/home/student/access_log' WITH DELIMITER=' ';



CREATE TABLE Request_line_details (IP_Address text, time text,method text, path text, protocol text, PRIMARY KEY(path,IP_Address,time,method,protocol));

COPY cloud_log.access_log (ip_address,time,request_line) TO 'requestline.csv' with DELIMITER = ' ' and QUOTE = ' ';

COPY cloud_log.request_line_details (IP_ADDRESS,time,method, path, protocol) FROM 'requestline.csv' WITH DELIMITER = ' ' and QUOTE = '"' and ESCAPE = '*';

--How many hits were made to the website item “/assets/img/release-schedule-logo.png”?
select count(*) from request_line_details where path = '/assets/img/release-schedule-logo.png';

--How many hits were made from the IP: 10.207.188.188?
select count(*) from cloud_log.access_log where IP_Address = '10.207.188.188' ;

--Which path in the website has been hit most? How many hits were made to the path?
select count(path) as path_count, path from request_line_details  group by path;

--Which IP accesses the website most? How many accesses were made by it?
select count(ip_address) as ip_count, ip_address from access_log group by ip_address;
