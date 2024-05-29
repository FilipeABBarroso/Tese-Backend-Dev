import json  
import requests

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/hsts?url={entity}"

    response = requests.get(url)
    data = json.loads(response.text)
    if "error" in data:
      dataToOutput["error"] = data["error"]
    else:
      if "message" in data:
        dataToOutput["message"] = data["message"]
      if "compatible" in data:
        dataToOutput["compatible"] = data["compatible"]
      if "hstsHeader" in data:
        dataToOutput["hstsHeader"] = data["hstsHeader"]
    
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput