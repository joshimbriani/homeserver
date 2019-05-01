import os
import json

coasters = []
parks = []

for filename in os.listdir("data"):
    if filename.endswith(".json"):
        with open("data/" + filename) as f:
            data = json.load(f)

            for coaster in data["coasters"]:
                coasters.append(coaster)

            for park in data["parks"]:
                parks.append(park)

combined = {}
combined["coasters"] = coasters
combined["parks"] = parks

with open('combined.json', 'w') as outfile:
    json.dump(combined, outfile)