import hug
import os
import json
from shapely import wkt
from urllib.parse import urlparse
from db import (
    db_connect,
    import_co2_data,
    query_level_2_data
)

print('Booting...')
pg_url = os.getenv(
   'DB_URL',
   'http://skyapi_development_user:pleasefortheloveofspaghettichangeme@127.0.0.1/skyapi_development'  # noqa
)
parsed = urlparse(pg_url)
db_config = {
   'host': parsed.hostname,
   'user': parsed.username,
   'password': parsed.password,
   'database': parsed.path[1:],
   'connect_timeout': 3
}
db_connection = db_connect(db_config)
print('Postgres connected with DB_URL={}'.format(pg_url))


@hug.get(query=hug.input_format.json)
def points(query):
    loaded = json.loads(query)
    if not loaded['from_time']:
        return {'error': 'from_time was not provided'}
    if not loaded['to_time']:
        return {'error': 'to_time was not provided'}
    polygon = wkt.loads(loaded['geo'])
    records = query_level_2_data(
        db_connection,
        polygon,
        loaded['from_time'],
        loaded['to_time']
    )
    return [{
       'time': r[2],
       'geo': 'POINT({} {})'.format(*r[3]),
       'data_fields': r[4]
    } for r in records]


@hug.cli(version='0.0.0')
def import_data():
    '''imports all files in the ./data folder'''
    data_folder = './data'
    path = os.path.abspath(data_folder)
    filenames = sorted([f for f in os.listdir(path) if f[-3:] == '.h5'])
    skipped = 0
    for filename in filenames:
        print('Importing {}'.format(filename))
        if not import_co2_data(db_connection, os.path.join(path, filename)):
            skipped += 1
    return 'Imported {} files\n{} files skipped'.format(
        len(filenames) - skipped,
        skipped
    )


if __name__ == '__main__':
    import_data.interface.cli()
