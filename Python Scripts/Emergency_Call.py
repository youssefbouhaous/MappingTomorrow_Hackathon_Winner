import time
import random
import csv
from arcgis.gis import GIS

# Connection to your ArcGIS Online account
gis = GIS("https://www.arcgis.com", "oussamasig", "SigGisoussama860")

# Load the shapefile polygon
shapefile_path = r"C:\Users\Oussama\Desktop\datachicago\chicago_Polygone.shp"
shape = shapefile.Reader(shapefile_path)
shape_records = shape.shapeRecords()

# Prepare a list of polygon geometries
polygon_geometries = [record.shape for record in shape_records]

while True:
    time.sleep(10)

    # Generate a random point until it's within any of the polygons
    while True:
        random_point = (random.uniform(-180, 180), random.uniform(-90, 90))  # Assuming latitudes and longitudes

        point_within_polygon = False
        for polygon in polygon_geometries:
            # Checking if the random point is within the bounding box of the polygon
            if (polygon.bbox[0] <= random_point[0] <= polygon.bbox[2] and
                    polygon.bbox[1] <= random_point[1] <= polygon.bbox[3]):
                # It's within the bounding box, consider it's within the polygon
                point_within_polygon = True
                break

        if point_within_polygon:
            break

    x, y = random_point
    print(x, y)

    # Create a CSV file with the random point's coordinates
    csv_file = "Emergency_Call.csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x', 'y'])
        writer.writerow([x, y])

    # Get the item by its ID for overwriting
    item_id = "1c155c837971464cbdb6107f98ad4d82"  # Replace with the actual item ID
    item = gis.content.get(item_id)

    # Update the existing item with the new CSV file data
    updated_item = item.update(data=csv_file)
