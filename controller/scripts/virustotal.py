import json  
import requests

def runTest(entity):
  url = "https://www.virustotal.com/api/v3/domains/" + entity

  headers = {"accept": "application/json", "x-apikey": "4a45ecc1c266b1f687746efd10ed568e4826daf842c5b28a801dfb8b4637b531"}

  response = requests.get(url, headers=headers)
  '''save_file = open("outputs/savedata-virustotal.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  '''
  data = json.loads(response.text)
  dataToOutput = {"entity": entity}
  dataToOutput["malicious analysis"] = data["data"]["attributes"]["last_analysis_stats"]["malicious"]
  dataToOutput["suspicious analysis"] = data["data"]["attributes"]["last_analysis_stats"]["suspicious"]
  dataToOutput["undetected analysis"] = data["data"]["attributes"]["last_analysis_stats"]["undetected"]
  dataToOutput["harmless analysis"] = data["data"]["attributes"]["last_analysis_stats"]["harmless"]
  return dataToOutput