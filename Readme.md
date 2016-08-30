# Sky API

### How are the points aligned to coordinates? (top left or center)
[AIRS Level 3 Readme](http://acdisc.gesdisc.eosdis.nasa.gov/data/Aqua_AIRS_Level3/AIRS3C2M.005/doc/AIRS_V5_Tropospheric_CO2_Products.pdf)

### How do we load h5 in java?
[H5File Format](https://www.hdfgroup.org/products/java/hdf-java-html/javadocs/ncsa/hdf/object/h5/H5File.html)

### Which L3 datasets on Mirador are useful for high resolution ghg info?
[MIRADOR API](http://mirador.gsfc.nasa.gov/cgi-bin/mirador/servcoll.pl?helpmenuclass=inventory&SearchButton=Search%20GES-DISC)
[example access form](http://acdisc.gesdisc.eosdis.nasa.gov/opendap/Aqua_AIRS_Level3/AIRX3C2M.005/2012/AIRS.2012.02.01.L3.CO2Std029.v5.9.14.0.X12089140931.hdf.html)

### Which L3 datasets do we need to request that would be useful?
[Copernicus](https://co2.jpl.nasa.gov/)?

### Which internationally accepted anthropogenic greenhouse gases?
- carbon dioxide (CO2)
http://acdisc.gsfc.nasa.gov/data/Aqua_AIRS_Level3/AIRS3C28.005/2016/ 2.5 x 2 deg
http://acdisc.gsfc.nasa.gov/data/Aqua_AIRS_Level3/AIRS3C2D.005/2016/ 2.5 x 2 deg
http://acdisc.gsfc.nasa.gov/data/Aqua_AIRS_Level3/AIRS3C2M.005/2016/ 2.5 x 2 deg
- methane (CH4) - Not on Mirador
- nitrous oxide (N2O)
http://measures.gesdisc.eosdis.nasa.gov/data/GOZCARDS/GozMmlpN2O.1/ 10 deg zonal
http://measures.gesdisc.eosdis.nasa.gov/data/GOZCARDS/GxozSmlpN2O.1/ 10 deg zonal
http://acdisc.gesdisc.eosdis.nasa.gov/data/Aura_HIRDLS_Level3/H3ZFCN2O.007/ 1 deg lat zonal
- sulfur hexafluoride (SF6) - Not on Mirador
- hydrofluorocarbons (HFCs) - Not on Mirador
- perfluorocarbons (PFCs) - Not on Mirador

The data on Ceres is very updated
http://terra.nasa.gov/data/ceres-data


### What is the format of the Mirador ASCII dump?

### How do we get NASA credentials?
[NASA Data Cookbook](http://disc.sci.gsfc.nasa.gov/recipes/?q=recipe-cookbook)

### Can we download data automatically?
Use wget for bulk downloads?
Pretend to be a real user with [nightmarejs](http://www.nightmarejs.org/)?

MOPITT
https://www2.acom.ucar.edu/mopitt/publications
https://www2.acom.ucar.edu/mopitt/products

## API Questions

### What types of queries does the api need to support?
- Geo: Land masses are not rectangles. Shapes! One reading that contains a point?
- Time: range?
- Reading: specific spectroscopy band?
- Satellite: only satellites in list?

## API Proposal

### Level 2 Call Format

The API functions by posting JSON to an endpoint
Geo queries are an array of [latitude, longitude] pairs.
Dates are in ISO 8601 in UTC.

```bash
curl -X POST \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type:application/json" \
  -d '{"geo":[[-71.1043443253471,-42.3150676015829],[71.1043443253471,-42.3150676015829],[71.1043443253471,42.3150676015829],[-71.1043443253471,42.3150676015829],[-71.1043443253471,-42.3150676015829]],"from_time":"2016-08-23T17:23:05.070Z","to_time":"2016-08-23T17:23:05.070Z","data_fields":["CO2ret"],"satellite":["AIRS"]}' \
  https://endpoint.example.com/skyapi
```

### Level 2 Return Format

- root response: array of readings
  - time: time of the reading
  - point: a (latitude, longitude) pair representing the center of the reading
  - data_fields: an object of field ids
    - $field_id: an object keyed by the requested data fields

```json
[{
	"time": "2016-07-31T23:00:00.000Z",
	"point": [27.53, 36.41],
	"data_fields": {
    "CO2ret": 401.142
	}
}]
```

## Testing

start h5serv before running tests
```bash
sudo docker run -p 5000:5000 -d -v `pwd`/tests/data:/data splacorn/h5serv:aac69032aa9abd596e9ea7897372d86472d9be0d --domain=skyapi.wenzowski.com
```

then run tests
```bash
pytest
```
