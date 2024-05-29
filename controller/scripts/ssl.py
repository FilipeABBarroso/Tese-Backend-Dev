import json  
import requests

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/ssl?url={entity}"

    response = requests.get(url)
    data = json.loads(response.text)
    if "error" in data:
      dataToOutput["error"] = data
    else:
      dataToOutput["subject C"] = data["subject"]["C"]
      dataToOutput["subject ST"] = data["subject"]["ST"]
      dataToOutput["subject O"] = data["subject"]["O"]
      dataToOutput["subject CN"] = data["subject"]["CN"]
      dataToOutput["issuer CN"] = data["issuer"]["CN"]
      dataToOutput["issuer O"] = data["issuer"]["O"]
      dataToOutput["issuer CN"] = data["issuer"]["CN"]
      dataToOutput["ca"] = data["ca"]
      dataToOutput["valid from"] = data["valid_from"]
      dataToOutput["valid to"] = data["valid_to"]
      dataToOutput["fingerprint"] = data["fingerprint"]
      dataToOutput["fingerprint256"] = data["fingerprint256"]
      dataToOutput["fingerprint512"] = data["fingerprint512"]
      dataToOutput["serialNumber"] = data["serialNumber"]
    
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput