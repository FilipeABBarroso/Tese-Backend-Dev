import json  
import requests

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/security-txt?url={entity}"

    response = requests.get(url)
    data = json.loads(response.text)
    if "error" in data:
      dataToOutput["error"] = data["error"]
    else:
      dataToOutput["TXT Security present"] = data["isPresent"]
      if "foundIn" in data:
        dataToOutput["found In"] = data["foundIn"]
      if "content" in data:
        dataToOutput["content"] = data["content"]
      if "isPgpSigned" in data:
        dataToOutput["isPgpSigned"] = data["isPgpSigned"]
    
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput