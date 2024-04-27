import json  
import requests

def getTechStack(entity):
  url = f"https://web-check.xyz/api/tech-stack?url={entity}"
  response = requests.get(url)
  save_file = open("outputs/savedata-techStack.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")