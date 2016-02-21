import argparse
import urllib2
import time
import json
import sys
import csv

base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"

def parse_nearby_search_json(response_json, results_accumulator):
	to_return = None
	if "next_page_token" in response_json:
		to_return = response_json["next_page_token"]
	for result in response_json["results"]:
		results_accumulator.append({
			"id": result["place_id"],
			"name": result["name"].encode("ascii", "ignore"),
			"vicinity": result["vicinity"]
		})

	return to_return

def nearby_search(key, lat, lon, radius=100, type="restaurant"):
	base_query = base_url
	base_query += "key=" + key + "&"
	base_query += "location=" + lat + "," + lon + "&"
	base_query += "radius=" + str(radius) + "&"
	base_query += "type=" + type

	response = urllib2.urlopen(base_query).read()
	response_json = json.loads(response)
	to_return = []
	next_page_token = parse_nearby_search_json(response_json, to_return)
	while next_page_token:
		next_query = base_query + "&pagetoken=" + next_page_token
		time.sleep(2)
		next_page_token = parse_nearby_search_json(json.loads(urllib2.urlopen(next_query).read()), to_return)

	return to_return

parser = argparse.ArgumentParser(description="CLI for Google Nearby Search API")
parser.add_argument("--key", default="AIzaSyBsFW5OElYgEZFaNjt1AyFVCaRRLNjWXLI")
parser.add_argument("--lat", required=True)
parser.add_argument("--long", required=True)
parser.add_argument("--radius", default=100)
args = parser.parse_args()

results = nearby_search(args.key, args.lat, args.long, args.radius)

with sys.stdout as csvout:
	fieldnames = ["name", "id", "vicinity"]
	writer = csv.DictWriter(csvout, fieldnames=fieldnames)
	writer.writerows(results)	
