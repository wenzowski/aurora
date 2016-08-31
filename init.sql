CREATE USER skyapi_development_user WITH PASSWORD 'pleasefortheloveofspaghettichangeme';
CREATE DATABASE skyapi_development;
GRANT ALL PRIVILEGES ON DATABASE skyapi_development to skyapi_development_user;
\connect skyapi_development;
CREATE EXTENSION postgis;
CREATE EXTENSION hstore;
CREATE TABLE level_2_data (
  id SERIAL PRIMARY KEY,
  time TIMESTAMP WITHOUT TIME ZONE,
  point GEOMETRY(Polygon,4326),
  data_fields HSTORE
);
# still need compound index level_2_data_time_point
