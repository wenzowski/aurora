import pytest
from db import (
    db_connect,
    format_sql_time,
    format_sql_point,
    format_sql_data_fields,
    format_sql,
    insert_rows,
    insert_row
)
import datetime


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
def db_cursor(db_connection):
    return db_connection.cursor()


@pytest.fixture
def extracted_co2_data_fields():
    return {
        'time': '2016-06-01T00:00:00.000Z',
        'point': [29.219999, 24.93],
        'data_fields': {
            'avg_kern': [1.29526801e-04],  # 100-element list
            'co2_ret': 411.54401,
            'co2_std': 1.806
        }
    }


def test_db_connect(config):
    from psycopg2.extensions import connection
    db = db_connect(config)
    assert type(db) is connection
    assert db.dsn == 'dbname=skyapi_test user=skyapi_test_user password=xxxxxxxx host=localhost'  # noqa


# TODO: check column type of point & data
def test_has_level_2_data_table(db_cursor):
    sql = '''
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = 'level_2_data';
    '''
    #  sql = '''
    #  SELECT level_2_data FROM sky_dai_test;
    #  '''
    db_cursor.execute(sql)
    result = db_cursor.fetchall()
    # assert result == [
    #     ('id', 'integer'),
    #     ('time', 'timestamp without time zone'),
    #     ('point', 'geometry(geometry,4326)'),
    #     ('data_fields', 'hstore')
    # ]
    assert result == [
        ('id', 'integer'),
        ('time', 'timestamp without time zone'),
        ('point', 'USER-DEFINED'),
        ('data_fields', 'USER-DEFINED')
    ]


def test_format_sql_time(extracted_co2_data_fields):
    time = extracted_co2_data_fields['time']
    sql_time = format_sql_time(time)
    assert sql_time == ('%s', '2016-06-01T00:00:00.000Z')


def test_format_sql_point(extracted_co2_data_fields):
    point = extracted_co2_data_fields['point']
    sql_point = format_sql_point(point)
    #  geometry ST_Point(float x_lon, float y_lat);
    assert sql_point == (
        'ST_SetSRID(ST_Point(%s, %s),4326)',
        24.93,
        29.219999
    )


def test_format_sql_data_fields(extracted_co2_data_fields):
    data_fields = extracted_co2_data_fields['data_fields']
    sql_data_fields = format_sql_data_fields(data_fields)
    assert sql_data_fields == (
        '\'"avg_kern" => "%s","co2_ret" => "%s","co2_std" => "%s"\'',
        [0.000129526801],  # how will psycopg2 cast this?
        411.54401,
        1.806
    )


def test_format_sql(extracted_co2_data_fields):
    sql = format_sql(**extracted_co2_data_fields)
    assert sql == (
        'INSERT INTO level_2_data (time, point, data_fields)'
        'VALUES ('
        '%s,'
        'ST_SetSRID(ST_Point(%s, %s),4326),'
        '\'"avg_kern" => "%s","co2_ret" => "%s","co2_std" => "%s"\''
        ');',
        (
            '2016-06-01T00:00:00.000Z',
            24.93,
            29.219999,
            [0.000129526801],
            411.54401,
            1.806
        )
    )


#  options:
#  https://github.com/yohanboniface/psycopg-postgis
#  https://github.com/geoalchemy/geoalchemy2
def test_insert_row(db_connection, extracted_co2_data_fields):
    import psycopg2.extras
    assert insert_row(db_connection, extracted_co2_data_fields) is True
    sql_select = 'SELECT time, point, data_fields FROM level_2_data LIMIT 1'
    db_cursor = db_connection.cursor()
    psycopg2.extras.register_hstore(db_cursor)
    db_cursor.execute(sql_select)
    result = db_cursor.fetchall()
    assert result == [
        (
            datetime.datetime(2016, 6, 1, 0, 0),
            '0101000020E6100000AE47E17A14EE38401827BEDA51383D40',
            {
                'avg_kern': 'ARRAY[0.000129526801]',
                'co2_ret': '411.54401',
                'co2_std': '1.806'
            }
        )
    ]


def test_insert_rows(db_connection, extracted_co2_data_fields):
    fields_list = [
        extracted_co2_data_fields,
        extracted_co2_data_fields
    ]
    assert insert_rows(db_connection, fields_list) is True
