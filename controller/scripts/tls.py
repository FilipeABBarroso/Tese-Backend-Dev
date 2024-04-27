import json  
import requests

def runTest(entity):
  url = f"https://web-check.xyz/api/tls?url={entity}"

  response = requests.get(url)
  '''save_file = open("outputs/savedata-tls.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  '''
  return json.loads(response.text)