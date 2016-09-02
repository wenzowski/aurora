import pytest
import numpy
from os.path import abspath
from co2 import open_h5_reader, cast_tai_to_utc_string, extract_co2_data_fields


@pytest.fixture
def airs_file():
    path = abspath('tests/data/AIRS.2016.05.31.240.L2.CO2_Std_IR.v5.4.11.0.CO2.T16160193514.h5')  # noqa
    return open_h5_reader(path)


def test_co2_groups_exist(airs_file):
    co2 = airs_file['/CO2']
    assert [key for key in co2] == [
        'Data Fields', 'Geolocation Fields', 'Swath Attributes'
    ]


def test_cast_tai_to_utc_string():
    assert cast_tai_to_utc_string(7.388928e+08) == '2016-06-01T00:00:00.000Z'


def test_co2_can_be_read(airs_file):
    readings = extract_co2_data_fields(airs_file)
    expected = {
        'time': '2016-06-01T00:00:00.000Z',
        'point': [29.219999, 24.93],
        'data_fields': {
            'avg_kern': [1.29526801e-04],  # 100-element list
            'co2_ret': 411.54401,
            'co2_std': 1.806
        }
    }
    assert readings[0]['time'] == expected['time']
    assert numpy.isclose(readings[0]['point'][0], expected['point'][0])
    assert numpy.isclose(readings[0]['point'][1], expected['point'][1])
    assert numpy.isclose(
        readings[0]['data_fields']['co2_ret'],
        expected['data_fields']['co2_ret']
    )
    assert numpy.isclose(
        readings[0]['data_fields']['co2_std'],
        expected['data_fields']['co2_std']
    )
    assert numpy.isclose(
       readings[0]['data_fields']['avg_kern'][0],
       expected['data_fields']['avg_kern'][0]
    )
