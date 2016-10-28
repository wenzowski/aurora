# Aurora

### Installation on Ubuntu 16.04
```bash
# apt-get update
# apt-get install -y postgis libpq-dev make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils
# adduser app
# cd /home/app && su app
$ git clone https://github.com/yyuu/pyenv.git ~/.pyenv
$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
$ echo 'eval "$(pyenv init -)"' >> ~/.bashrc
$ exec $SHELL
$ git clone https://github.com/wenzowski/aurora.git ~/aurora && cd $_
$ pyenv install `cat .python-version`
$ pip install -r requirements.txt
```

### Download Data from NASA

1.  Register with [Earthdata](https://wiki.earthdata.nasa.gov/display/EL/How+To+Register+With+Earthdata+Login)
2.  [Add GES DISC Authorization](http://disc.sci.gsfc.nasa.gov/registration/authorizing-gesdisc-data-access-in-earthdata_login)
3.  Use your credentials to authenticate

    ```bash
    $ touch ~/.urs_cookies && chmod 600 ~/.urs_cookies
    $ touch ~/.netrc && chmod 600 ~/.netrc
    $ echo "machine urs.earthdata.nasa.gov login <uid> password <password>" >> ~/.netrc
    ```
    where <uid> is your user name and <password> is your URS password without the brackets
    ```bash
    $ cd ~/aurora/data
    $ pv ~/sources/*.txt | xargs -n 1 -P 50 -I % wget --content-disposition --no-check-certificate --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --auth-no-challenge=on --keep-session-cookies --prefer-family=IPv4 -q %


### Convert h4 files to h5 files

    ```bash
    $ ls *.hdf | xargs -I{} sh -c "h4toh5 {}"
    $ rm *.hdf
    $ hug -f server.py -c import_data # actually import the data
    ```


## API Proposal

### Level 2 Call Format

The API relies on JSON query documents, which are escaped by the browser's
`encodeURIComponent()` before being sent as a query variable.

Query document structure:
- `geo`: a wkt string defining the area to return readings for.
- `from_time`: an ISO 8601 string representing the start of the time period.
- `to_time`: an ISO 8601 string representing the end of the time period.

Note that while the WKT coordinate system uses `[longitude, latitude]`,
not all coordinate systems are [lonlat].

```bash
curl -X GET \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type:application/json" \
  https://endpoint.example.com/points?query=`
    node -e 'console.log(encodeURIComponent(JSON.stringify(
      {
        "geo": "POLYGON((21.61 18.87, 21.63 18.87, 21.63 18.89, 21.61 18.89, 21.61 18.87))",
        "from_time":"2016-06-01T00:03:00Z",
        "to_time":"2016-06-01T00:04:00Z",
        "readings":["co2_ret"],
        "satellite":["AIRS"]
      }
    )))'`
```

### Level 2 Return Format

- root response: array of readings
  - `time`: time of the reading
  - `geo`: a wkt string compatible with the ISO/IEC 13249-3:2011 standard
  - `readings`: an object of field ids
    - `$field_id`: an object keyed by the requested data fields

```json
[{
	"time": "2016-07-31T23:00:00.000Z",
	"geo": "POINT(21.62, 18.88)",
	"readings": {
    "co2_ret": 401.142
	}
}]
```
## Testing

```bash
$ pytest
```

### Building list of AIRS data
```bash
$ wget --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --auth-no-challenge=on --keep-session-cookies -r -c -nH -nd -np -A hdf "http://airsl2.gesdisc.eosdis.nasa.gov/data/Aqua_AIRS_Level2/AIRS2SPC.005/" --spider -o wget.txt
$ grep ^-- wget.txt | cut -d\  -f4 | grep \.hdf$ | uniq > ~/aurora/sources/AIRS2SPCv5.txt
```

[lonlat]: http://www.macwright.org/lonlat/
