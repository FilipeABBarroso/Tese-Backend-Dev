import json  
import requests

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/robots-txt?url={entity}"

    response = requests.get(url)
    data = json.loads(response.text)
    if "error" in data:
      dataToOutput["error"] = json.loads(data)["error"]
    else:
      dataToOutput["robots"] = data["robots"]
    
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput