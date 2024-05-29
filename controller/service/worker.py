from database.queries import *
import json
from datetime import datetime
import asyncio
import subprocess
import os
import importlib.util

async def worker():
  while True:
    try:
      campaigns = await getActiveCampaigns()
      for campaign in campaigns:
        if type(campaign["nextRun"]) == list:
          date = datetime.strptime(campaign["nextRun"][0], "%Y-%m-%dT%H:%M:%S.%fZ")
          runs = campaign["nextRun"][1:]
        else:
          date = datetime.strptime(json.loads(campaign["nextRun"])[0], "%Y-%m-%dT%H:%M:%S.%fZ")
          runs = json.loads(campaign["nextRun"])[1:]
        if(date < datetime.now()):
          startTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
          tag = campaign["tag"]
          formatted_date = date.strftime('%Y-%m-%d-%H-%M-%S')
          cte = await get_cte_id(tag)
          tests = await get_campaign_tests(tag)
          entities = await get_campaign_entities(tag)
          tasks = [run_test(test, entities) for test in tests]
          results = await asyncio.gather(*tasks)
          concatenated_json = {}
          for result in results:
            concatenated_json.update(result)
          path = f'outputs/{tag}-result-{formatted_date}.json'
          with open(path, "w") as save_file:
            json.dump(concatenated_json, save_file, indent=6)
            save_file.close()
          await update_campaign_and_create_result(tag, runs, cte, path, startTime)
    except Exception as e:
       print(f"worker error: {e}")
    await asyncio.sleep(60)

async def run_test(test, entities):
    script_name = test['script']
    script_path = os.path.join('controller', 'scripts', script_name)
    
    # Check if script exists
    if not os.path.exists(script_path):
        return f"Script {script_name} não encontrado."
    
    # Importing script module
    try:
        spec = importlib.util.spec_from_file_location(script_name.replace('.py', ''), script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        return f"Erro ao importar o script {script_name}: {str(e)}"
    
    # Check if the runTest function exists
    if not hasattr(module, 'runTest') or not callable(module.runTest):
        return f"A função runTest não foi encontrada no script {script_name}."
    
    # Exec function
    try:
        result = []
        if "internetnl" in script_name: 
           result = module.runTest(entities)
        else:
          for entity in entities:
            result.append(module.runTest(entity["url"]))
        return {script_name: result}
    except Exception as e:
        return f"Erro ao executar a função do script {script_name}: {str(e)}"