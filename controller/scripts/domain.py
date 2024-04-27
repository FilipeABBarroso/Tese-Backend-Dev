import json  
import requests

def getDomain(entity):
  url = f"https://web-check.xyz/api/domain?url={entity}"

  response = requests.get(url)
  print("No info in domain", response.text)
  if response.status_code == 200:
    save_file = open("outputs/savedata-domain.json", "w")  
    json.dump(json.loads(response.text), save_file, indent = 6)  
    save_file.close()  
  else: 
    print("No info in domain")
  print("Done!")