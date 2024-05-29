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
  try:
    dataToOutput["entity type"] = data["data"]["type"]
    dataToOutput["malicious analysis"] = data["data"]["attributes"]["last_analysis_stats"]["malicious"]
    dataToOutput["suspicious analysis"] = data["data"]["attributes"]["last_analysis_stats"]["suspicious"]
    dataToOutput["undetected analysis"] = data["data"]["attributes"]["last_analysis_stats"]["undetected"]
    dataToOutput["harmless analysis"] = data["data"]["attributes"]["last_analysis_stats"]["harmless"]
    dataToOutput["last https certificate date"] = data["data"]["attributes"]["last_https_certificate_date"]
    dataToOutput["last analysis date"] = data["data"]["attributes"]["last_analysis_date"]
    dataToOutput["reputation"] = data["data"]["attributes"]["reputation"]
    dataToOutput["last dns records date"] = data["data"]["attributes"]["last_dns_records_date"]
    dataToOutput["whois"] = data["data"]["attributes"]["whois"]
    dataToOutput["last https certificate public key algorithm"] = data["data"]["attributes"]["last_https_certificate"]["public_key"]["algorithm"]
    dataToOutput["https validity end date"] = data["data"]["attributes"]["last_https_certificate"]["validity"]["not_after"]
    dataToOutput["https validity start date"] = data["data"]["attributes"]["last_https_certificate"]["validity"]["not_before"]
    dataToOutput["version"] = data["data"]["attributes"]["last_https_certificate"]["version"]
    dataToOutput["https extensions CA"] = data["data"]["attributes"]["last_https_certificate"]["extensions"]["CA"]
    dataToOutput["https cert signature algorithm"] = data["data"]["attributes"]["last_https_certificate"]["cert_signature"]["signature_algorithm"]
    dataToOutput["https cert signature"] = data["data"]["attributes"]["last_https_certificate"]["cert_signature"]["signature"]
    dataToOutput["https serial number"] = data["data"]["attributes"]["last_https_certificate"]["serial_number"]
    dataToOutput["categories"] = data["data"]["attributes"]["categories"]["BitDefender"]
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput