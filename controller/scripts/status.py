import json  
import requests

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/status?url={entity}"

    response = requests.get(url)
    data = json.loads(response.text)
    if "error" in data:
      dataToOutput["error"] = data["error"]
    else:
      dataToOutput["is up"] = data["isUp"]
      dataToOutput["response time"] = data["responseTime"]
      dataToOutput["response code"] = data["responseCode"]
    
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput