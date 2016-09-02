import pytest
from db import (
    SortedJson,
    import_co2_data,
    db_connect,
    db_cursor,
    format_sql_point,
    format_sql_data_fields,
    format_sql,
    insert_rows,
    insert_row
)
import numpy
import datetime
from postgis import Point


@pytest.fixture
def config():
    return {
        'host': 'localhost',
        'user': 'skyapi_test_user',
        'password': 'password',
        'database': 'skyapi_test'
    }


@pytest.fixture
def db_connection(config):
    return db_connect(config)


@pytest.fixture
def extracted_co2_data_fields():
    return {
        'time': '2016-06-01T00:00:00.000Z',
        'point': [29.219999, 24.93],
        'data_fields': {
            'avg_kern': numpy.array([1.29526801e-04], dtype='float32'),  # 100-element list
            'co2_ret': 411.54401,
            'co2_std': 1.806
        }
    }


def test_import_co2_data(db_connection):
    h5_path = 'tests/data/AIRS.2016.05.31.240.L2.CO2_Std_IR.v5.4.11.0.CO2.T16160193514.h5'  # noqa
    inserted_ids = import_co2_data(db_connection, h5_path)
    assert type(inserted_ids) is list
    for id in inserted_ids:
        assert type(id) is int


def test_db_connect(config):
    from psycopg2.extensions import connection
    db = db_connect(config)
    assert type(db) is connection
    assert db.dsn == 'dbname=skyapi_test user=skyapi_test_user password=xxxxxxxx host=localhost'  # noqa


# TODO: check column type of point & data
def test_has_level_2_data_table(db_connection):
    sql = '''
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = 'level_2_data';
    '''
    cursor = db_cursor(db_connection)
    cursor.execute(sql)
    result = cursor.fetchall()
    assert result == [
        ('id', 'integer'),
        ('time', 'timestamp without time zone'),
        ('point', 'USER-DEFINED'),  # why isn't this 'geometry(geometry,4326)'?
        ('data_fields', 'jsonb')
    ]


#  https://github.com/yohanboniface/psycopg-postgis/blob/master/postgis/point.py
def test_format_sql_point(extracted_co2_data_fields):
    point = extracted_co2_data_fields['point']
    sql_point = format_sql_point(point)
    y_lat, x_lon = point
    assert sql_point == Point(x_lon, y_lat, srid=4326)


def test_format_sql_data_fields(extracted_co2_data_fields):
    data_fields = extracted_co2_data_fields['data_fields']
    sql_data_fields = format_sql_data_fields(data_fields)
    assert type(sql_data_fields) == SortedJson


def test_format_sql(db_connection, extracted_co2_data_fields):
    cursor = db_cursor(db_connection)
    sql_template = \
        'INSERT INTO level_2_data (time, point, data_fields)' + \
        'VALUES (%s, %s, %s) RETURNING id;'
    sql_values = format_sql(**extracted_co2_data_fields)
    sql = cursor.mogrify(sql_template, sql_values)
    assert sql == b'INSERT INTO level_2_data (time, point, data_fields)VALUES (\'2016-06-01T00:00:00.000Z\', ST_GeometryFromText(\'POINT(24.93 29.219999)\', 4326), \'{"avg_kern": [0.00012952680117450655], "co2_ret": 411.54401, "co2_std": 1.806}\') RETURNING id;'  # noqa


#  options:
#  https://github.com/yohanboniface/psycopg-postgis
#  https://github.com/geoalchemy/geoalchemy2
def test_insert_row(db_connection, extracted_co2_data_fields):
    id = insert_row(db_connection, extracted_co2_data_fields)
    assert type(id) is int
    sql_select = 'SELECT time, point, data_fields FROM level_2_data WHERE id = %s LIMIT 1'
    cursor = db_cursor(db_connection)
    cursor.execute(sql_select, (id,))
    result = cursor.fetchall()
    assert result == [
        (
            datetime.datetime.strptime(
                '2016-06-01T00:00:00Z',
                '%Y-%m-%dT%H:%M:%SZ'
            ),
            Point(24.93, 29.219999),
            {
                'avg_kern': [0.00012952680117450655],
                'co2_ret': 411.54401,
                'co2_std': 1.806
            }
        )
    ]


def test_insert_rows(db_connection, extracted_co2_data_fields):
    fields_list = [
        extracted_co2_data_fields,
        extracted_co2_data_fields
    ]
    inserted_ids = insert_rows(db_connection, fields_list)
    assert type(inserted_ids) is list
    for id in inserted_ids:
        assert type(id) is int
        sql_select = 'SELECT time, point, data_fields FROM level_2_data WHERE id = %s LIMIT 1'
        cursor = db_cursor(db_connection)
        cursor.execute(sql_select, (id,))
        result = cursor.fetchall()
        assert result == [
            (
                datetime.datetime.strptime(
                    '2016-06-01T00:00:00Z',
                    '%Y-%m-%dT%H:%M:%SZ'
                ),
                Point(24.93, 29.219999),
                {
                    'avg_kern': [0.00012952680117450655],
                    'co2_ret': 411.54401,
                    'co2_std': 1.806
                }
            )
        ]
