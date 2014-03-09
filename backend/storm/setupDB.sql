CREATE USER 'storm_user'@'localhost' IDENTIFIED BY 'storm_pass';
GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER
    ON storm.*
    TO 'storm_user'@'localhost';