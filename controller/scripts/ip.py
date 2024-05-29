import json  
import requests

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/get-ip?url={entity}"

    response = requests.get(url)
    data = json.loads(response.text)
    if "error" in data:
      dataToOutput["error"] = data["error"]
    else:
      if "ip" in data:
        dataToOutput["ip"] = data["ip"]
      if "family" in data:
        dataToOutput["family"] = data["family"]
    
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput