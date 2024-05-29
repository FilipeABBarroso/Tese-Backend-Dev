import json  
import requests

def runTest(entity):
  url = f"https://web-check.xyz/api/tls?url={entity}"

  response = requests.get(url)
  '''save_file = open("outputs/savedata-tls.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  '''
  data = json.loads(json.loads(response.text))
  dataToOutput = {"entity": entity}
  try:
    dataToOutput["has tls"] = data["has_tls"]
    dataToOutput["cert id"] = data["cert_id"]
    dataToOutput["trust id"] = data["trust_id"]
    dataToOutput["is valid"] = data["is_valid"]
    dataToOutput["completion perc"] = data["completion_perc"]
    dataToOutput["connection serverside"] = data["connection_info"]["serverside"]
    dataToOutput["completion ciphersuite protocols"] = data["connection_info"]["ciphersuite"][0]["protocols"]
    dataToOutput["completion ciphersuite pubkey"] = data["connection_info"]["ciphersuite"][0]["pubkey"]
    if "analysis" in data:
      for obj in data["analysis"]:
        if "analyzer" in obj and obj["analyzer"] == "awsCertlint":
          dataToOutput["awsCertlint bugs result"] = obj["result"]["bugs"]
          dataToOutput["awsCertlint errors result"] = obj["result"]["errors"]
          dataToOutput["awsCertlint notices errors"] = obj["result"]["notices"]
          dataToOutput["awsCertlint warnings errors"] = obj["result"]["warnings"]
          dataToOutput["awsCertlint fatalErrors errors"] = obj["result"]["fatalErrors"]
          dataToOutput["awsCertlint informational errors"] = obj["result"]["informational"]
        if obj["analyzer"] and obj["analyzer"] == "mozillaGradingWorker":
          dataToOutput["mozillaGradingWorker grade result"] = obj["result"]["grade"]
          dataToOutput["mozillaGradingWorker failures result"] = obj["result"]["failures"]
          dataToOutput["mozillaGradingWorker lettergrade result"] = obj["result"]["lettergrade"]
    dataToOutput["ack"] = data["ack"]
    
  except:
    if "error" in data:
      dataToOutput["error"] = data["error"]
    else:
      dataToOutput["error"] = "data not found"
  return dataToOutput