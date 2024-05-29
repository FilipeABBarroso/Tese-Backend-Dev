import json  
import requests
import time

def runTest():
  headers = {"Authorization": "Basic ZmlsaXBlLmJhcnJvc286NkZDTmNhakpHVG9SelROMg=="}
  url = "https://batch.internet.nl/api/batch/v2/requests"
  
  dataToOutput = {}

  payloadWeb = {
    "domains": [
      "example.com",
      "google.com"
    ],
    "name": "First test",
    "type": "web"
  }

  payloadMail = {
    "domains": [
      "example.com",
      "google.com"
    ],
    "name": "First test",
    "type": "mail"
  }
  try:
    responseWeb = requests.post(url, headers=headers, json=payloadWeb)
    responseMail = requests.post(url, headers=headers, json=payloadMail)
    idWeb = responseWeb.json()["request"]["request_id"]
    idMail = responseMail.json()["request"]["request_id"]
    print("id: ", id)
    time.sleep(480)
    urlWeb = f"https://batch.internet.nl/api/batch/v2/requests/{idWeb}/results"
    urlMail = f"https://batch.internet.nl/api/batch/v2/requests/{idMail}/results"
    responseWeb = requests.get(urlWeb, headers=headers)
    responseMail = requests.get(urlMail, headers=headers)
    if responseWeb.status_code == 200 and responseMail.status_code == 200:
      dataWeb = responseWeb.json()
      dataMail = responseMail.json()
      dataToOutput["Web data"] = dataWeb
      dataToOutput["MAil data"] = dataMail
    else: 
      dataToOutput["error"] = "Request error"
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput