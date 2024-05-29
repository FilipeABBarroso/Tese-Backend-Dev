import json  
import requests

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/redirects?url={entity}"

    response = requests.get(url)
    data = json.loads(response.text)
    if "error" in data:
      dataToOutput["error"] = data["error"]
    else:
      dataToOutput["redirects"] = data["redirects"]
    
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput