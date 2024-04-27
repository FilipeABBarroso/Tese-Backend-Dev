import json  
import requests

def getIP(entity):
  url = f"https://web-check.xyz/api/get-ip?url={entity}"

  #headers = {"accept": "application/json", "x-apikey": "4a45ecc1c266b1f687746efd10ed568e4826daf842c5b28a801dfb8b4637b531"}

  response = requests.get(url)
  print(response.json)
  save_file = open("outputs/savedata-ip.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()    
  print("Done!")