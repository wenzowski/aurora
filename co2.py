import h5py
import calendar
import datetime


def open_h5_reader(absolute_path):
    return h5py.File(absolute_path, 'r')


def cast_tai_to_utc_string(tai_seconds):
    #  here's how we derive the tai_epoch
    #  note that we have not accounted for leap seconds
    #  tai_epoch = time.strptime('1993-01-01T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    #  tai_epoch_unix = calendar.timegm(tai_epoch)
    tai_epoch_unix = float(725846400)
    utc_seconds = tai_epoch_unix + tai_seconds
    utc_datetime = datetime.datetime.fromtimestamp(utc_seconds)
    return utc_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'


def extract_co2_data_fields(airs_file):
    avg_kern = airs_file['/CO2/Data Fields/AvgKern']
    co2_ret = airs_file['/CO2/Data Fields/CO2ret']
    co2_std = airs_file['/CO2/Data Fields/CO2std']
    lat = airs_file['/CO2/Geolocation Fields/Latitude']
    lon = airs_file['/CO2/Geolocation Fields/Longitude']
    time = airs_file['/CO2/Geolocation Fields/Time']
    readings_list = []
    for x in range(co2_ret.shape[0]):
        for y in range(co2_ret.shape[1]):
            reading = co2_ret[x][y]
            if reading != -9999.0:
                readings_list.append({
                    'time': cast_tai_to_utc_string(time[x][y]),
                    'point': [lat[x][y], lon[x][y]],
                    'data_fields': {
                        'avg_kern': avg_kern[x][y].flatten(),
                        'co2_ret': co2_ret[x][y],
                        'co2_std': co2_std[x][y]
                    }
                })
    return readings_list
