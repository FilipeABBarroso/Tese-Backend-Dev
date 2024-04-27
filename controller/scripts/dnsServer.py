import json  
import requests

def getDnsServer(entity):
  url = f"https://web-check.xyz/api/dns-server?url={entity}"

  response = requests.get(url)
  save_file = open("outputs/savedata-dnsServer.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")