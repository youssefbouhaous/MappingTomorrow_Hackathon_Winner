import shapefile
from arcgis.geometry import Polyline
from arcgis.gis import GIS
import networkx as nx
import random
import numpy as np
from os import remove
import json

# Connect to your ArcGIS Online account
gis = GIS("https://www.arcgis.com", "oussamasig", "SigGisoussama860")

# Read the Roads shapefile from your local machine
roads_shapefile_path = r"C:\Users\Oussama\Desktop\datachicago\Chicago_roads.shp"
sf = shapefile.Reader(roads_shapefile_path)


polyline = Polyline({"paths": []}) 

# Create a graph representation of the road network
G = nx.Graph()
for shape_rec in sf.shapeRecords():
    for i in range(len(shape_rec.shape.points) - 1):
        start = shape_rec.shape.points[i]
        end = shape_rec.shape.points[i + 1]
        # Add the start and end nodes as they represent road intersections
        G.add_node(start)
        G.add_node(end)
        # Add edges representing the road connections
        G.add_edge(start, end)
    csv_item = gis.content.search("title:Emergency_Call", item_type="CSV")[0]
    csv_file = r"C:\Users\Oussama\Downloads\Emergency_Call.csv"       

try:
    remove(csv_file)  # Remove the existing file
except FileNotFoundError:
    pass

csv_item.download(save_path=r"C:\Users\Oussama\Downloads")


# Read the first point from the CSV file
with open(csv_file, 'r') as file:
    lines = file.readlines()
    x1, y1 = map(float, lines[1].strip().split(','))  # Assuming the file has a header line



# Generate random points or take them from the Emergency Call CSV file
x2, y2 = random.uniform(0, 100), random.uniform(0, 100)

def get_closest_node(graph, point):
    distances = [(n, np.linalg.norm(np.array(point) - np.array(n))) for n in graph.nodes()]
    closest = min(distances, key=lambda x: x[1])
    return closest[0]

source_node = get_closest_node(G, (x1, y1))
target_node = get_closest_node(G, (x2, y2))

# Find the shortest path in the network between the two closest nodes
try :
    shortest_path = nx.shortest_path(G, source=source_node, target=target_node)
except :
    print("Path Impossible")

json_way_file = "E_way.json"

features = []
coordinates = [[point[0], point[1]] for point in shortest_path]

# Create a GeoJSON Feature with LineString geometry type
feature = {
    "type": "Feature",
    "geometry": {
        "type": "LineString",
        "coordinates": coordinates
    },
    "properties": {}  # You can add any additional properties if needed
}

features.append(feature)

feature_collection = {
    "type": "FeatureCollection",
    "features": features
}

with open(json_way_file, 'w') as file:
    json.dump(feature_collection, file)

# Get the item by its ID for overwriting
item_id = "371b844be6be4925be3383795c8e58e6"  # Replace with the actual item ID
item = gis.content.get(item_id)
print(item)

# Update the existing item with the new GeoJSON file data
updated_item = item.update(data=json_way_file)
print("Updated")
