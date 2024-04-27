import json  
import requests

def getfirewall(entity):
  url = f"https://web-check.xyz/api/firewall?url={entity}"

  response = requests.get(url)
  save_file = open("outputs/savedata-firewall.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")