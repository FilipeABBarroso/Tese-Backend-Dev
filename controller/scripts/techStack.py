import json  
import requests

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/tech-stack?url={entity}"
    response = requests.get(url)
    data = json.loads(response.text)
    if "error" in data:
      dataToOutput["error"] = data["error"]
    else:
      dataToOutput["data"] = data
    
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput