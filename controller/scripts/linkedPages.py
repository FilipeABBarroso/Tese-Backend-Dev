import json  
import requests

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/linked-pages?url={entity}"

    response = requests.get(url)
    data = json.loads(response.text)
    if "error" in data:
      dataToOutput["error"] = data["error"]
    else:
      if "internal" in data:
        for i, mxRecord in enumerate(data["internal"], start=1):
          dataToOutput[f"internal linked page {i}"] = mxRecord
      if "external" in data:
        for i, mxRecord in enumerate(data["external"], start=1):
          dataToOutput[f"external linked page {i}"] = mxRecord
    
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput