import pytest
import h5py
import numpy
from os.path import abspath


@pytest.fixture
def airs_file():
    path = 'tests/data/public/AIRS.2016.05.31.240.L2.CO2_Std_IR.v5.4.11.0.CO2.T16160193514.h5'  # noqa
    return h5py.File(abspath(path), 'r')


def test_co2_groups_exist(airs_file):
    co2 = airs_file['/CO2']
    assert [key for key in co2] == [
        'Data Fields', 'Geolocation Fields', 'Swath Attributes'
    ]


def test_co2_can_be_read(airs_file):
    readings = []
    avg_kern = airs_file['/CO2/Data Fields/AvgKern']
    co2_ret = airs_file['/CO2/Data Fields/CO2ret']
    co2_std = airs_file['/CO2/Data Fields/CO2std']
    lat = airs_file['/CO2/Geolocation Fields/Latitude']
    lon = airs_file['/CO2/Geolocation Fields/Longitude']
    time = airs_file['/CO2/Geolocation Fields/Time']
    for x in range(co2_ret.shape[0]):
        for y in range(co2_ret.shape[1]):
            reading = co2_ret[x][y]
            if reading != -9999.0:
                readings.append({
                    'time': time[x][y],
                    'point': [lat[x][y], lon[x][y]],
                    'data_fields': {
                        'avg_kern': avg_kern[x][y].flatten(),
                        'co2_ret': co2_ret[x][y],
                        'co2_std': co2_std[x][y]
                    }
                })
    expected = {
        'time': 7.388928e+08,
        'point': [29.219999, 24.93],
        'data_fields': {
            'avg_kern': [1.29526801e-04],  # 100-element list
            'co2_ret': 411.54401,
            'co2_std': 1.806
        }
    }
    assert numpy.isclose(readings[0]['time'], expected['time'])
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
