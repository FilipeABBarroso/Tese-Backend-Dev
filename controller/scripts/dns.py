import json  
import requests

def getDns(entity):
  url = f"https://web-check.xyz/api/dns?url={entity}"

  response = requests.get(url)
  save_file = open("outputs/savedata-dns.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")