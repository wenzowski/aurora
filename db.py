import psycopg2
import psycopg2.extras
import postgis
import json
import decimal
import numpy
import os.path
from co2 import (
    open_h5_reader,
    extract_co2_data_fields
)


psycopg2.extensions.register_adapter(
    dict, psycopg2.extras.Json
)


def db_connect(config):
    return psycopg2.connect(**config)


def db_cursor(db_connection):
    cursor = db_connection.cursor()
    postgis.register(cursor)
    return cursor


def check_is_dataset_imported(db_connection, filename):
    sql = 'SELECT EXISTS(SELECT 1 FROM imported_files WHERE filename=%s)'
    cursor = db_cursor(db_connection)
    cursor.execute(sql, (filename,))
    return cursor.fetchone()[0]


def begin_import(db_connection, filename):
    sql = 'INSERT INTO imported_files (filename) ' + \
        'VALUES (%s) RETURNING id;'
    cursor = db_cursor(db_connection)
    cursor.execute(sql, (filename,))
    return cursor.fetchone()[0]  # note: still need to commit()


def format_sql_point(point):
    return postgis.Point(point[1], point[0], srid=4326)


class DbEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)  # shouldn't we rangeerror or something?
        if isinstance(o, (numpy.ndarray, numpy.generic)):
            return o.tolist()
        return super(DbEncoder, self).default(o)


class SortedJson(psycopg2.extras.Json):
    def dumps(self, obj):
        return json.dumps(obj, sort_keys=True, cls=DbEncoder)


def format_sql_data_fields(data_fields):
    return SortedJson(data_fields)


def format_sql(time='', point=[], data_fields={}):
    if time == '':
        raise ValueError('time is required')
    if not point:
        raise ValueError('point is required')
    if data_fields == {}:
        raise ValueError('data_fields is required')
    return (
        time,
        format_sql_point(point),
        format_sql_data_fields(data_fields)
    )


def insert_row(db_connection, file_id, fields):
    sql_format = \
        'INSERT INTO level_2_data (file_id, time, point, data_fields) ' + \
        'VALUES (%s, %s, %s, %s) RETURNING id;'
    time, point, data_fields = format_sql(**fields)
    sql_values = (file_id, time, point, data_fields)
    cursor = db_cursor(db_connection)
    cursor.execute(sql_format, sql_values)
    id = cursor.fetchone()[0]
    db_connection.commit()
    return id


def insert_rows(db_connection, filename, fields_list):
    file_id = begin_import(db_connection, filename)
    inserts_format = ','.join(('(%s,%s,%s,%s)' for x in fields_list))
    sql_format = \
        'INSERT INTO level_2_data (file_id, time, point, data_fields) ' + \
        'VALUES ' + inserts_format + ' RETURNING id;'
    cursor = db_cursor(db_connection)
    values_list = []
    for fields in fields_list:
        values_list.append(file_id)
        for value in format_sql(**fields):
            values_list.append(value)
    cursor.execute(sql_format, values_list)
    ids = cursor.fetchall()
    db_connection.commit()
    return [id[0] for id in ids]


def import_co2_data(db_connection, h5_path):
    path = os.path.abspath(h5_path)
    file_name = os.path.basename(h5_path)
    airs_file = open_h5_reader(path)
    fields_list = extract_co2_data_fields(airs_file)
    return insert_rows(db_connection, file_name, fields_list)


def query_level_2_data(db_connection, lat_lon_list, from_time, to_time):
    sql_select = '''
    SELECT id, file_id, time, point, data_fields
    FROM level_2_data
    WHERE ST_Within(point, ST_GeomFromText(%s)::geography::geometry)
    AND time > %s
    AND time < %s
    LIMIT 1;
    '''
    cursor = db_cursor(db_connection)
    lon_lat = ','.join(
        (str(float(lon)) + ' ' + str(float(lat)) for lat, lon in lat_lon_list)
    )
    lon_lat_str = 'POLYGON(('+ lon_lat +'))'
    cursor.execute(sql_select, (lon_lat_str, from_time, to_time))
    return cursor.fetchall()
