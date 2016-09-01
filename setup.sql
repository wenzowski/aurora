-- make a new user that owns a development database
-- sudo -u postgres psql -f ./setup.sql
CREATE USER skyapi_development_user WITH PASSWORD 'pleasefortheloveofspaghettichangeme';
CREATE DATABASE skyapi_development;
GRANT ALL PRIVILEGES ON DATABASE skyapi_development to skyapi_development_user;
CREATE USER skyapi_test_user WITH PASSWORD 'password';
CREATE DATABASE skyapi_test;
GRANT ALL PRIVILEGES ON DATABASE skyapi_test to skyapi_test_user;
\c skyapi_test
CREATE EXTENSION postgis;
\c skyapi_development
CREATE EXTENSION postgis;
