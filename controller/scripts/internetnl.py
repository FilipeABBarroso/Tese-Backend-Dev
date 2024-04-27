import json  
import requests
import time

def getInternetNL():
  headers = {"Authorization": "Basic ZmlsaXBlLmJhcnJvc286NkZDTmNhakpHVG9SelROMg=="}
  url = "https://batch.internet.nl/api/batch/v2/requests"
  

  payload = {
    "domains": [
      "example.com",
      "google.com"
    ],
    "name": "First test",
    "type": "mail"
  }



  #responseWeb = requests.post(url, headers=headers, json=payload)
  responseMail = requests.post(url, headers=headers, json=payload)
  id = responseMail.json()["request"]["request_id"]
  print("id: ", id)
  time.sleep(480)
  url = f"https://batch.internet.nl/api/batch/v2/requests/{id}/results"
  response = requests.get(url, headers=headers)
  print("results: ", response.json())
  if response.status_code == 200:
    save_file = open("outputs/savedata-internetNL-MailResult.json", "w")  
    json.dump(response.json(), save_file, indent = 6)  
    save_file.close()  
  else: 
    print("No info in Archives")
  print("Done!")