import json  
import requests

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/dns-server?url={entity}"

    response = requests.get(url)
    data = json.loads(response.text)
    if "error" in data:
      dataToOutput["error"] = data["error"]
    else:
      for i, dns in enumerate(data["dns"], start=1):
        dataToOutput[f"address{i}"] = dns["address"]
        dataToOutput[f"dohDirectSupports{i}"] = dns["dohDirectSupports"]
        if dns["hostname"]:
          for j, hostname in enumerate(dns["hostname"], start=1):
            dataToOutput[f"hostname{i}_{j}"] = hostname
        else:
          dataToOutput[f"hostname{i}"] = None
    
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput