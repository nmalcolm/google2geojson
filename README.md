# google2geojson

## The Problem

Google doesn't make it easy to use your Saved Places with third party software. If you export your Saved Places with Google Takeout it'll give you a CSV file of links to Google Maps. These links sometimes include coordinates in the URL, but if you've saved an existing location (e.g. Empire State Building) it doesn't include any useful information.

## The Solution

This repo contains two scripts. The first is `fetch.py` which parses any coordinates from the Google Maps links and uses [chromedriver](https://googlechromelabs.github.io/chrome-for-testing/#stable) to visit and extract the coordinates from Google Maps links which don't include coordindates. A new CSV file will be created, essentially a copy of the original CSV file but with all coordindates.

The second script is `csv2geojson.py`. You can use this one to convert the new CSV file to a `geojson` file which can be used with GQIS and other spatial software.

## Installation

```
pip install -r requirements.txt
```

You'll also need [chromedriver](https://googlechromelabs.github.io/chrome-for-testing/#stable) installed and in your `PATH`.

## Usage

```
python fetch.py Whatever.csv

python csv2geojson.py Whatever_with_coords.csv
```

## License

Released under the MIT License. See LICENSE.
