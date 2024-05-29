import json  
import requests

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/rank?url={entity}"

    response = requests.get(url)
    data = json.loads(response.text)
    if "error" in data:
      dataToOutput["error"] = data["error"]
    else:
      if "skipped" in data:
        dataToOutput["skipped"] = data["skipped"]
      if "rank" in data:
        dataToOutput["rank"] = data["rank"]
      if "date" in data:
        dataToOutput["date"] = data["date"]
    
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput