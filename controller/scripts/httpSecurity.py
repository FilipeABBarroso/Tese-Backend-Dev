import json  
import requests

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/http-security?url={entity}"

    response = requests.get(url)
    data = json.loads(response.text)
    if "error" in data:
      dataToOutput["error"] = data["error"]
    else:
      if "strictTransportPolicy" in data:
        dataToOutput["strictTransportPolicy"] = data["strictTransportPolicy"]
      if "xFrameOptions" in data:
        dataToOutput["xFrameOptions"] = data["xFrameOptions"]
      if "xContentTypeOptions" in data:
        dataToOutput["xContentTypeOptions"] = data["xContentTypeOptions"]
      if "xXSSProtection" in data:
        dataToOutput["xXSSProtection"] = data["xXSSProtection"]
      if "contentSecurityPolicy" in data:
        dataToOutput["contentSecurityPolicy"] = data["contentSecurityPolicy"]
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput