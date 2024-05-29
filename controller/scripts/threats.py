import json  
import requests

def runTest(entity):
  url = f"https://web-check.xyz/api/threats?url={entity}"

  response = requests.get(url)
  data = json.loads(response.text)
  dataToOutput = {"entity": entity}
  try:
    dataToOutput["urlHaus query status"] = data["urlHaus"]["query_status"]
    dataToOutput["phishTank"] = data["phishTank"]["url0"]["in_database"]
    dataToOutput["cloudmersive"] = data["cloudmersive"]
    dataToOutput["unsafe Browsing"] = data["safeBrowsing"]["unsafe"]
    
  except:
    if "error" in data:
      dataToOutput["error"] = data["error"]
    else:
      dataToOutput["error"] = "Data not found"
  return dataToOutput