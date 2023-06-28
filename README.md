```
░██████╗░███████╗░█████╗░██████╗░██╗███╗░░██╗░█████╗░███████╗██████╗░
██╔════╝░██╔════╝██╔══██╗██╔══██╗██║████╗░██║██╔══██╗██╔════╝██╔══██╗
██║░░██╗░█████╗░░██║░░██║██████╔╝██║██╔██╗██║██║░░╚═╝█████╗░░██████╔╝
██║░░╚██╗██╔══╝░░██║░░██║██╔═══╝░██║██║╚████║██║░░██╗██╔══╝░░██╔══██╗
╚██████╔╝███████╗╚█████╔╝██║░░░░░██║██║░╚███║╚█████╔╝███████╗██║░░██║
░╚═════╝░╚══════╝░╚════╝░╚═╝░░░░░╚═╝╚═╝░░╚══╝░╚════╝░╚══════╝╚═╝░░╚═╝
```

GeoPincer is a script that leverages OpenStreetMap's Overpass API in order to search for locations. These locations will be queried using a collection of establishments that are somewhat adjacent.

# Usage
Requires a base area to search for along with at least two nodes (establishments/ notable places) that are semi-adjacent:   
   
	python3 GeoPincer.py "Texas" "Office Depot" "Sam's Club"

The script uses a default range of 500 meters between the nodes. This can be changed using the `--distance` argument: 

	python3 GeoPincer.py "Texas" "Office Depot" "Sam's Club" --distance 300
	
> Note: Use lower distances like 300 or 200 meters if your locations are within walking distance

For large-range searches, you can use the provided U.S. region dictionaries in order to query `Northeast`, `West`, `Midwest`, `South`, or all four with keyword `US`:
	
	python3 GeoPincer.py "US" "Office Depot" "Sam's Club" "Burlington"

# Output
Any locations that match your query will be returned as Google Maps URLs:

```
$python3 GeoPincer.py "Maryland" "Shell" "Holiday Inn" --distance 500
Searching Maryland...


https://www.google.com/maps/search/?q=39.4912534%2C-76.6488350
https://www.google.com/maps/search/?q=39.0204488%2C-76.9266807
https://www.google.com/maps/search/?q=39.1720764%2C-76.7868042
https://www.google.com/maps/search/?q=39.2871907%2C-76.7319217
https://www.google.com/maps/search/?q=38.9828586%2C-76.5408389
https://www.google.com/maps/search/?q=39.2729241%2C-76.6284725
https://www.google.com/maps/search/?q=38.8207627%2C-76.9164325
https://www.google.com/maps/search/?q=38.4401860%2C-75.5633542
https://www.google.com/maps/search/?q=39.4778553%2C-76.2496829
```