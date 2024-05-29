import json  
import requests

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/archives?url={entity}"

    response = requests.get(url)
    data = json.loads(response.text)
    if "error" in data:
      dataToOutput["error"] = data["error"]
    else:
      if "firstScan" in data:
        dataToOutput["firstScan"] = data["firstScan"]
      if "lastScan" in data:
        dataToOutput["lastScan"] = data["lastScan"]
      if "totalScans" in data:
        dataToOutput["totalScans"] = data["totalScans"]
      if "changeCount" in data:
        dataToOutput["changeCount"] = data["changeCount"]
      if "averagePageSize" in data:
        dataToOutput["averagePageSize"] = data["averagePageSize"]
      if "scanFrequency" in data:
        if "daysBetweenScans" in data["scanFrequency"]:
          dataToOutput["daysBetweenScans"] = data["scanFrequency"]["daysBetweenScans"]
        if "daysBetweenChanges" in data["scanFrequency"]:
          dataToOutput["daysBetweenChanges"] = data["scanFrequency"]["daysBetweenChanges"]
        if "scansPerDay" in data["scanFrequency"]:
          dataToOutput["scansPerDay"] = data["scanFrequency"]["scansPerDay"]
        if "changesPerDay" in data["scanFrequency"]:
          dataToOutput["changesPerDay"] = data["scanFrequency"]["changesPerDay"]
    
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput