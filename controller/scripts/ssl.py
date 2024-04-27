import json  
import requests

def getSSL(entity):
  url = f"https://web-check.xyz/api/ssl?url={entity}"
  response = requests.get(url)
  save_file = open("outputs/savedata-ssl.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")