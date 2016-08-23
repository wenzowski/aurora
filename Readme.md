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

## API Questions

### Should we minimize transfer size or optimize for readability?
Choice: n-tuple arrays vs nested objects

## API Proposal

### Return Format

The API will always return a (latitude, longitude) pair which is represents the center of the reading.
- lat: latitude of the top left corner of rectangular area
- lon: longitude of the top left corner of rectangular area

```json
[
  {
    "lat": 30.5,
    "lon": 50.0,
    "data": {
      "co2": 50,
      "ch4": 50
    }
  },
  {
    "lat": 31.5,
    "lon": 50.0,
    "data": {
      "co2": 49,
      "ch4": 51
    }
  }
}
```

