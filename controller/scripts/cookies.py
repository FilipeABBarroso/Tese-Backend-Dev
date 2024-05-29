import json  
import requests

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/cookies?url={entity}"
  
    response = requests.get(url)
    data = json.loads(response.text)
    if "error" in data:
      dataToOutput["error"] = data["error"]
    else:
      if "skipped" in data:
        dataToOutput["Skipped"] = data["skipped"]
      else:
        if "clientCookies" in data:
          dataToOutput["Client_Cookies"] = data["clientCookies"]
        if "headerCookies" in data:
          for i, c in enumerate(data["headerCookies"], start=1):
            dataToOutput[f"headerCookies_{i}"] = c
    
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput