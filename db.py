import psycopg2
import psycopg2.extras
import postgis


def db_connect(config):
    return psycopg2.connect(**config)


def db_cursor(db_connection):
    cursor = db_connection.cursor()
    psycopg2.extras.register_hstore(cursor)
    postgis.register(cursor)
    return cursor


def format_sql_time(time):
    return ("%s", time)


def format_sql_point(point):
    return (
        'ST_SetSRID(ST_Point(%s, %s),4326)',
        point[1],
        point[0]
    )


def format_sql_data_fields(data_fields):
    format_string_items = []
    data_values = []
    for k, v in sorted(data_fields.items()):
        format_string_items.append('"'+k+'" => "%s"')
        data_values.append(v)
    format_string = ','.join(format_string_items)
    format_string = "'" + format_string + "'"
    return (
        format_string,
        *data_values
    )


def format_sql(time='', point=[], data_fields={}):
    if time == '':
        raise ValueError('time is required')
    if not point:
        raise ValueError('point is required')
    if data_fields == {}:
        raise ValueError('data_fields is required')
    sql_time_format, *sql_time_values = format_sql_time(time)
    sql_point_format, *sql_point_values = format_sql_point(point)
    sql_data_fields_format, *sql_data_fields_values = format_sql_data_fields(
        data_fields
    )
    format_string = \
        'INSERT INTO level_2_data (time, point, data_fields)' + \
        'VALUES (' + \
        sql_time_format + ',' + \
        sql_point_format + ',' + \
        sql_data_fields_format + \
        ');'
    return (
        format_string,
        (
            *sql_time_values,
            *sql_point_values,
            *sql_data_fields_values
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
