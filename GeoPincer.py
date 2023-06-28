from urllib.parse import urlencode
import sys
import overpass                                     
import argparse
from tqdm import tqdm
import geopy.distance

def get_locations(area, nodes, distance, max_results=None):
	nodes_list = nodes[:]
	api = overpass.API(timeout=600)
	
	query = f'area[name~"{area}"]->.searchArea;'

	first_node = nodes_list.pop(0)

	query += f'nw["name"]["name"~"{first_node}",i](area.searchArea)->.a;'

	for node in nodes:
		query += f'nw["name"](around.a:{distance})["name"~"{node}",i];'

	query+= "out center;"

	response = api.get(query, responseformat="csv(::lat,::lon)")

	while ['',''] in response: response.remove(['',''])
	location_list = []

	for element in response:
		if element not in location_list:
			location_list.append(element)
		if max_results and len(location_list) > max_results:
			break

	#Removing any possible duplicate locations
	num_locs = len(location_list)
	return_list = []
	for i in range(1, num_locs):
			valid_loc = True

			for j in range(i+1, num_locs):
				loc_distance = geopy.distance.geodesic((float(location_list[i][0]),float(location_list[i][1])), \
				 (float(location_list[j][0]), float(location_list[j][1]))).m

				if loc_distance < distance*2:
					valid_loc = False
					break

			if valid_loc:
				return_list.append(location_list[i])
	return return_list

def get_google_maps_url(lat, lon):
	query_parameters = {"q": f"{lat},{lon}"}
	url = "https://www.google.com/maps/search/?" + urlencode(query_parameters)
	return url

def valid_region(region):
	with open('regions.txt') as f:
		regions = eval(f.read())
		for key, value in regions.items():
			if key == region:
				return True
	return False

def use_regions(region, nodes, distance, max_results):
	print(f'Running on region: {region}')
	location_list = []
	urls = []
	with open('regions.txt') as f:
		regions = eval(f.read())
		for key, value in regions.items():
			if key == region:
				location_list = value
	
	for location in tqdm(location_list):

		location_array = get_locations(location, nodes, distance, max_results)
		if location_array:
			for coords in location_array:
				urls.append((get_google_maps_url(coords[0], coords[1])))
	return urls

def parse_arguments():
	parser = argparse.ArgumentParser(description='Find locations that contain your nodes within a certain radius')
	parser.add_argument('area', type=str, help='Area to search from ex. State, City, Town, etc.')
	parser.add_argument('nodes', type=str, nargs='+', help='Names of the places(nodes) for the search')
	parser.add_argument('--distance', type=int, default=500, help='Distance between nodes in meters (default: 500)')
	parser.add_argument('--max-results', type=int, help="Maximum number of results to retrieve")
	example_use_case = 'Example: python3 GeoPincer.py "Maryland" "Holiday Inn" "Shell" --distance 1000 --max-results 5 '
	parser.epilog = example_use_case
	return parser.parse_args()

def main():
	args = parse_arguments()
	area = args.area 
	nodes = args.nodes 
	distance = args.distance 
	max_results = args.max_results

	if (valid_region(area)):
		urls = use_regions(area, nodes, distance, max_results)

	elif area == "US":
		print("Searching United States... (this will take ~20 minutes)\n")
		urls = use_regions("Northeast", nodes, distance, max_results)
		urls += use_regions("South", nodes, distance, max_results)
		urls += use_regions("West", nodes, distance, max_results)
		urls += use_regions("Midwest", nodes, distance, max_results)

	else:
		print(f'Searching {area}...\n')
		locations = get_locations(area, nodes, distance, max_results)
		urls = [get_google_maps_url(location[0], location[1]) for location in locations]

	print()
	if not urls:
		print("Could not find any locations.\nMake sure parameters are spelled correctly and increase distance if needed.")
	for url in urls:
		print(url)

if __name__ == "__main__":
	main()


