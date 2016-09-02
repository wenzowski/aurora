import psycopg2
import psycopg2.extras
import postgis
from postgis import Point
import json
import numpy
from os.path import abspath
from co2 import open_h5_reader, cast_tai_to_utc_string, extract_co2_data_fields

def get_file(file_path):
    return open_h5_reader(abspath[file_path])  # noqa

def read_co2_data(data_file):
    readings = extract_co2_data_fields(data_file)
    return readings
    #expected = {
    #    'time': '2016-06-01T00:00:00.000Z',
    #    'point': [29.219999, 24.93],
    #    'data_fields': {
    #        'avg_kern': [1.29526801e-04],  # 100-element list
    #        'co2_ret': 411.54401,
    #        'co2_std': 1.806
    #    }
    #}
    #assert readings[0]['time'] == expected['time']
    #assert numpy.isclose(readings[0]['point'][0], expected['point'][0])
    #assert numpy.isclose(readings[0]['point'][1], expected['point'][1])
    #assert numpy.isclose(
        #readings[0]['data_fields']['co2_ret'],
        #expected['data_fields']['co2_ret']
    #)
    #assert numpy.isclose(
        #readings[0]['data_fields']['co2_std'],
        #expected['data_fields']['co2_std']
    #)
    #assert numpy.isclose(
       #readings[0]['data_fields']['avg_kern'][0],
       #expected['data_fields']['avg_kern'][0]
    #)

psycopg2.extensions.register_adapter(
    dict, psycopg2.extras.Json
)


def db_connect(config):
    return psycopg2.connect(**config)


def db_cursor(db_connection):
    cursor = db_connection.cursor()
    postgis.register(cursor)
    return cursor


def format_sql_point(point):
    return Point(point[1], point[0], srid=4326)


class SortedJson(psycopg2.extras.Json):
    def dumps(self, obj):
        return json.dumps(obj, sort_keys=True)


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
        'INSERT INTO level_2_data (time, point, data_fields)'
        'VALUES (%s, %s, %s);',
        (
            time,
            format_sql_point(point),
            format_sql_data_fields(data_fields)
        )
    )


def insert_row(db_connection, fields):
    sql_format, sql_values = format_sql(**fields)
    cursor = db_cursor(db_connection)
    cursor.execute(sql_format, sql_values)
    db_connection.commit()
    return True


def insert_rows(db_connection, fields_list):
    cursor = db_cursor(db_connection)
    cursor = db_connection.cursor()
    for fields in fields_list:
        sql_format, sql_values = format_sql(**fields)
        cursor.execute(sql_format, sql_values)
    db_connection.commit()
    return True
