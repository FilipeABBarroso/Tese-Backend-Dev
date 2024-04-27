import json  
import requests

def getScreenshot(entity):
  url = f"https://web-check.xyz/api/screenshot?url={entity}"

  response = requests.get(url)
  save_file = open("outputs/savedata-screenshot.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")