from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from sklearn.model_selection import train_test_split
from datetime import datetime

# existing data loading and preprocessing code
data_chic = pd.read_excel(r'C:\Users\Oussama\Desktop\datachicago\mini chicago.xlsx')  
data_chic['Date'] = pd.to_datetime(data_chic['Date'])
data_chic['Hour'] = data_chic['Date'].dt.hour
data_chic['Minute'] = data_chic['Date'].dt.minute
data_chic['Second'] = data_chic['Date'].dt.second
data_chic['Month'] = data_chic['Date'].dt.month
data_chic['Day'] = data_chic['Date'].dt.day
data_chic = data_chic.drop(['Date'], axis=1)
data_chic = data_chic.dropna()

# Split into features and targets
F = data_chic.drop(['X', 'Y'], axis=1)
T = data_chic[['X', 'Y']]

# Model training
F_train, F_test, T_train, T_test = train_test_split(F, T, test_size=0.2, random_state=42)
model_R = RandomForestRegressor(n_estimators=100)
model_R.fit(F_train, T_train)


def predict_coordinates(hour,minute, day, month) :
    user_input = pd.DataFrame({'Hour': [hour], 'Month': [month], 'Day': [day], 'Minute': [minute]})  # Include minutes in the user input
    prediction = model_R.predict(user_input[['Hour', 'Month', 'Day', 'Minute']])
    return prediction[0, 0],prediction[0, 1]




# Initialize your GIS with login credentials
gis = GIS("https://www.arcgis.com", "oussamasig", "SigGisoussama860")


def multiple_predictions(hour,minutes, day, month, nbr) :
    L=[]
    for i in range(nbr) :
        minutes+=10
        hour+=1
        if minutes >= 60 :
            minutes=0
            hour+=0.1
            if hour>=24 : 
                hour=0
                day+=1
                if day>=30 :
                    day=1
                    month+=1
                    if month>=12 : 
                        month=1
        P=predict_coordinates(hour,minutes, day, month)
        x=P[0]
        y=P[1]
        #print(x)
        #print(y)
        L.append([x,y])
    return L

# Function to update the existing JSON file with predicted crime coordinates
def update_json_with_predictions(predictions, item_id):
    # Initialize the features list
    features = []

    json_way_file = "E_way.json"
    
    features = []
    coordinates = [[point[0], point[1]] for point in predictions]

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
    item = gis.content.get(item_id)
    print(item)

    # Update the existing item with the new GeoJSON file data
    updated_item = item.update(data=json_way_file)
    print("Updated")

# Example usage: Updating the existing item with predicted crime coordinates
predicted_coords = multiple_predictions(hour=8,minutes=5, day=5, month=5, nbr=300)
item_id = "984af0647d4e4b77b2b3fdff5d809a12"  # Replace with the actual item ID
update_json_with_predictions(predicted_coords, item_id)
