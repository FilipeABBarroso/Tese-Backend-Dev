import requests

def getDmarcian(entity):
  api_url = "https://dmarcian.com/wp-admin/admin-ajax.php"

  payload = {
      "dns_query": f"_dmarcian.{entity}",
      "domain": entity,
  }

  response = requests.post(api_url, json=payload)
  print("here: ", response.text)

  if response.status_code == 200:
      print("Scan started successfully.")
      print(response.text)
  else:
      print("Error: Unable to start scan. Status code:", response.status_code)
