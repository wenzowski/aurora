# make a new user that owns a development database
# sudo -u postgres psql -f ./setup.sql
CREATE USER skyapi_development_user WITH PASSWORD 'pleasefortheloveofspaghettichangeme';
CREATE DATABASE skyapi_development;
GRANT ALL PRIVILEGES ON DATABASE skyapi_development to skyapi_development_user;
\c skyapi_development
CREATE EXTENSION postgis;
CREATE EXTENSION hstore;
