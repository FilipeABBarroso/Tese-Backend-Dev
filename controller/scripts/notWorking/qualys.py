import requests

def getQualys():
  api_url = "https://qualysguard.qg2.apps.qualys.eu/api/2.0/fo/scan/"

  username = "tcncs5fb"
  password = "4KrbDveN83HCP!U"

  target_url = "https://example.com"

  payload = {
      "url": target_url,
  }

  response = requests.get(api_url, auth=(username, password), json=payload)

  if response.status_code == 200:
      print("Scan started successfully.")
      print(response.text)
  else:
      print("Error: Unable to start scan. Status code:", response.status_code)
