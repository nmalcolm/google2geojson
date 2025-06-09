import csv
import json
import os
import sys

def csv_to_geojson(csv_file):
    base, _ = os.path.splitext(csv_file)
    geojson_file = f"{base}.geojson"
    features = []

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            lat = row.get("Latitude")
            lng = row.get("Longitude")

            if not lat or not lng:
                continue  # skip rows without coordinates

            try:
                lat = float(lat)
                lng = float(lng)
            except ValueError:
                continue

            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lng, lat]
                },
                "properties": {
                    key: row[key] for key in row if key not in ["Latitude", "Longitude"]
                }
            }
            features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(geojson_file, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    print(f"✅ GeoJSON saved to {geojson_file} with {len(features)} features.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python csv2geo.py <input_csv_file>")
        sys.exit(1)

    csv_input = sys.argv[1]
    csv_to_geojson(csv_input)
