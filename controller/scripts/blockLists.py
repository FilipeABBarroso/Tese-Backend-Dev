import json  
import requests

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/block-lists?url={entity}"

    response = requests.get(url)
    data = json.loads(response.text)
    if "error" in data:
      dataToOutput["error"] = data["error"]
    else:
      if "blocklists" in data:
        for block in data["blocklists"]:
          if "server" in block and "isBlocked" in block:
            dataToOutput[f'isBlocked_{block["server"]}'] = block["isBlocked"]
    
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput