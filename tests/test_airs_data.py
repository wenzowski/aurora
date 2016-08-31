import pytest
import numpy


@pytest.fixture
def airs_file():
    import h5pyd as h5py
    # there is one public/ folder at the root path
    mnt = h5py.File(
        'skyapi.wenzowski.com',  # default `host` domain
        'r',
        endpoint='http://localhost:5000'
    )
    return mnt['/public/AIRS.2016.05.31.240.L2.CO2_Std_IR.v5.4.11.0.CO2.T16160193514']  # noqa


def test_co2_groups_exist(airs_file):
    co2 = airs_file['/CO2']
    assert [key for key in co2] == [
        'Data Fields', 'Geolocation Fields', 'Swath Attributes'
    ]


def test_data_fields_can_be_read(airs_file):
    data_fields = airs_file['/CO2/Data Fields']
    assert [key for key in data_fields] == [
        'AvgKern',
        'CO2ret',
        'CO2std',
        'Day',
        'Hour',
        'LandFrac',
        'Minute',
        'Month',
        'Seconds',
        'Solzen',
        'Year'
    ]


def test_co2_can_be_read(airs_file):
    from h5pyd._hl.dataset import Dataset
    co2_data = airs_file['/CO2/Data Fields/CO2ret']
    assert co2_data.shape == (22, 15)
    assert type(co2_data) == Dataset
    assert co2_data[21][0][14] == -9999.0
    readings = []
    for x in range(co2_data.shape[0]):
        for y in range(co2_data.shape[1]):
            reading = co2_data[x][0][y]
            if reading != -9999.0:
                readings.append(reading)
    expected = [
        411.54401, 413.866, 403.534, 410.69199, 402.03699, 401.41199, 399.65601
    ]
    assert numpy.isclose(readings, expected).all()
