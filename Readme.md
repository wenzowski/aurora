# Sky API

###Installation
```bash
apt-get install -y postgis
apt-get install build-dep
```


### Where did we get the AIRS data?
http://airsl2.gesdisc.eosdis.nasa.gov/data/Aqua_AIRS_Level2/AIRS2SPC.005/

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

The API relies on JSON query documents, which are escaped by the browser's
`encodeURIComponent()` before being sent as a query variable.

Query document structure:
- `geo`: a [GeoJSON] document defining the area to return readings for.
- `from_time`: an ISO 8601 string representing the start of the time period.
- `to_time`: an ISO 8601 string representing the end of the time period.

Note that while the GeoJSON coordinate system uses `[longitude, latitude, elevation]`,
not all coordinate systems are [lonlat].

```bash
curl -X GET \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type:application/json" \
  https://endpoint.example.com/points?query=`
    node -e 'console.log(encodeURIComponent(JSON.stringify(
      {
        "geo": {
          "coordinates": [
            [21.61,18.87],[21.63,18.87],[21.63,18.89],[21.61,18.89],[21.61,18.87]
          ],
          "type":"Polygon"
        },
        "from_time":"2016-08-23T17:23:05.070Z",
        "to_time":"2016-08-23T17:23:05.070Z",
        "readings":["co2_ret"],
        "satellite":["AIRS"]
      }
    )))'`
```

### Level 2 Return Format

- root response: array of readings
  - `time`: time of the reading
  - `geo`: a [GeoJSON] document defining the geographic reference for the reading.
  - `readings`: an object of field ids
    - `$field_id`: an object keyed by the requested data fields

```json
[{
	"time": "2016-07-31T23:00:00.000Z",
	"geo": [
    "coordinates": [
      [21.62, 18.88]
    ],
    "type":"Point"
  ],
	"readings": {
    "co2_ret": 401.142
	}
}]
```

## Getting Data

```bash
wget -q -nH -nd http://airsl2.gesdisc.eosdis.nasa.gov/data/Aqua_AIRS_Level2/AIRS2STC.005/2016/152/ -O - | grep hdf\" | cut -f4 -d\" | xargs -I{} sh -c "wget http://airsl2.gesdisc.eosdis.nasa.gov/data/Aqua_AIRS_Level2/AIRS2STC.005/2016/152/{}"
ls *.hdf | xargs -I{} sh -c "h4toh5 {}"
rm *.hdf
hug -f server.py -c import_data # actually import the data
```

## Testing

```bash
pytest
```

[GeoJSON]: http://geojson.org/geojson-spec.html
[intro to GeoJSON]: http://www.macwright.org/2015/03/23/geojson-second-bite.html
[lonlat]: http://www.macwright.org/lonlat/
