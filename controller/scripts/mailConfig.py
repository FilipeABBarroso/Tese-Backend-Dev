import json  
import requests

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/mail-config?url={entity}"

    response = requests.get(url)
    data = json.loads(response.text)
    if "error" in data:
      dataToOutput["error"] = data["error"]
    else:
      if "skipped" in data:
        dataToOutput["skipped"] = data["skipped"]
      if "mxRecords" in data and "txtRecords" in data and "mailServices" in data and not (len(data["mxRecords"]) > 0 and len(data["txtRecords"]) > 0 and len(data["mailServices"]) > 0):
        dataToOutput["data"] = "No values found"
      if "mxRecords" in data:
        for i, mxRecord in enumerate(data["mxRecords"], start=1):
          if "exchange" in mxRecord:
            dataToOutput[f"mxRecords exchange {i}"] = mxRecord["exchange"]
          if "priority" in mxRecord:
            dataToOutput[f"mxRecords priority {i}"] = mxRecord["priority"]
      if "txtRecords" in data:
        for i, txtRecord in enumerate(data["txtRecords"], start=1):
          for j, record in enumerate(txtRecord, start=1):
            dataToOutput[f"txtRecords {i}.{j}"] = record
      if "mailServices" in data and len(data["mailServices"]) > 0:
        dataToOutput["mailServices"] = data["mailServices"]
        
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput