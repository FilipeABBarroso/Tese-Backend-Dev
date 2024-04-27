import os

def getPing(hostname):
  response = os.popen('ping -n 1 ' + hostname)
  linesNumb = len(response.readlines())
  if linesNumb > 1:
    print(f"{hostname} is up!")
  else:
    print(f"{hostname} is down!")