import json  
import requests

def getDnssec(entity):
  url = f"https://web-check.xyz/api/dnssec?url={entity}"

  response = requests.get(url)
  save_file = open("outputs/savedata-dnssec.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")