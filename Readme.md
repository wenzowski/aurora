# Sky API

### How are the points aligned to coordinates? (top left or center)
[AIRS Level 3 Readme](http://acdisc.gesdisc.eosdis.nasa.gov/data/Aqua_AIRS_Level3/AIRS3C2M.005/doc/AIRS_V5_Tropospheric_CO2_Products.pdf)

### How do we load h5 in java?
[H5File Format](https://www.hdfgroup.org/products/java/hdf-java-html/javadocs/ncsa/hdf/object/h5/H5File.html)

### Which L3 datasets on Mirador are useful for high resolution ghg info?
[MIRADOR API](http://mirador.gsfc.nasa.gov/cgi-bin/mirador/servcoll.pl?helpmenuclass=inventory&SearchButton=Search%20GES-DISC)

### Which L3 datasets do we need to request that would be useful?
[Copernicus](https://co2.jpl.nasa.gov/)?

### Which interationally accepted anthropogenic greenhouse gases?
- carbon dioxide (CO2)
- methane (CH4)
- nitrous oxide (N2O)
- sulfur hexafluoride (SF6)
- hydrofluorocarbons (HFCs)
- perfluorocarbons (PFCs)

MOPITT
https://www2.acom.ucar.edu/mopitt/publications
https://www2.acom.ucar.edu/mopitt/products

###Data Returned
Json:

lat1: lat coord of the top left corner of rectangular area
lng1: lng coord of the top left corner of rectangular area
lat2: lat coord of the bottom right corner of rectangular area
lng2: lng coord of the bottom right corner of rectangular area

```json
{ "areas": [
        "lat1": "30.5",
        "lng1": 50.0,
        "lat2": 31.5,
        "lng2": 51.0,
        "data": {
                "ghg": 50
        }
    ]`,
    [
        "lat1": "31.5",
        "lng1": 50.0,
        "lat2": 32.5,
        "lng2": 51.0,
        "data": {
                "ghg": 50
        }
    ]
}
```