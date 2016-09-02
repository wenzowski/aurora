-- this schema assumes postgres 9.5+ with postgis loaded
--
-- connect to existing database using credentials of db owner
-- sudo psql -f ./sql/schema.sql -U skyapi_development_user -h 127.0.0.1 skyapi_development
-- sudo psql -f ./sql/schema.sql -U skyapi_test_user -h 127.0.0.1 skyapi_test

CREATE TABLE IF NOT EXISTS imported_files (
  id serial PRIMARY KEY,
  filename text NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS imported_filename_index ON imported_files (filename);

CREATE TABLE IF NOT EXISTS level_2_data (
  id serial PRIMARY KEY,
  file_id integer NOT NULL REFERENCES imported_files (id) ON DELETE CASCADE,
  time timestamp without time zone NOT NULL,
  point geometry(Geometry,4326) NOT NULL,
  data_fields jsonb NOT NULL
);
-- still need compound index level_2_data_time_point
