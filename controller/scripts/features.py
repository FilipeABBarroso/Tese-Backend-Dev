import json  
import requests

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/features?url={entity}"

    response = requests.get(url)
    data = json.loads(response.text)
    if "Errors" in data:
      dataToOutput["error"] = data["Errors"][0]["Message"]
    else:
      if "groups" in data:
        for group in data["groups"]:
          if "categories" in group and "name" in group:
            for category in group["categories"]:
              if "name" in category and "live" in category:
                dataToOutput[f'{group["name"]}_{category["name"]}'] = category["live"]
          else:
            if "name" in group and "live" in group:
              dataToOutput[group["name"]] = group["live"]
    
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput