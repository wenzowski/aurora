-- connect to existing database using credentials of db owner
-- sudo psql -f ./init.sql -U skyapi_development_user -h 127.0.0.1 skyapi_development
-- sudo psql -f ./init.sql -U skyapi_test_user -h 127.0.0.1 skyapi_test
CREATE TABLE level_2_data (
  id SERIAL PRIMARY KEY,
  time TIMESTAMP WITHOUT TIME ZONE,
  point GEOMETRY(Geometry,4326),
  data_fields HSTORE
);
-- still need compound index level_2_data_time_point
