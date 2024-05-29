import json  
import requests

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/firewall?url={entity}"

    response = requests.get(url)
    data = json.loads(response.text)
    if "error" in data:
      dataToOutput["error"] = data["error"]
    else:
       if "hasWaf" in data:
        dataToOutput["hasWaf"] = data["hasWaf"]
       if "waf" in data:
        dataToOutput["waf"] = data["waf"]
    
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput