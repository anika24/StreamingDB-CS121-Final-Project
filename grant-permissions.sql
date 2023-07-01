-- To avoid warnings and errors
DROP USER IF EXISTS 'appadmin'@'localhost';
DROP USER IF EXISTS 'appclient'@'localhost';
FLUSH PRIVILEGES;

CREATE USER 'appadmin'@'localhost' IDENTIFIED BY 'adminpw';

CREATE USER 'appclient'@'localhost' IDENTIFIED BY 'clientpw';

-- Can add more users or refine permissions

GRANT ALL PRIVILEGES ON streamingdb.* TO 'appadmin'@'localhost';

GRANT SELECT ON streamingdb.* TO 'appclient'@'localhost';

FLUSH PRIVILEGES;
