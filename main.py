import requests
import json
import random

register_url = "http://localhost:8080/LifeGame.register"
process_url = "http://localhost:8080/LifeGame.process"
update_url = "http://localhost:8080/LifeGame.update"
unregister_url = "http://localhost:8080/LifeGame.unregister"

agentList = list()

headers = {'Content-Type': 'application/json'}
for x in range(0, 5):
    for y in range(0, 5):
        values = {"coordX": x, "coordY": y, "isAlive": False if (x + y) % 2 == 0 else True}
        # True if random.randint(0, 1) == 1 else False}
        agentList.append(values)
        r = requests.post(register_url, data=json.dumps(values), headers=headers)

for agent in agentList:
    r = requests.post(process_url, data=json.dumps(
        {"coordX": agent.get("coordX"), "coordY": agent.get("coordY"), "isAlive": agent.get("isAlive")}),
                      headers=headers)
    aliveCounter = 0
    for receivedAgent in json.loads(r.text).get("agentMessage"):
        if receivedAgent.get("isAlive"):
            aliveCounter += 1
    agentData = dict
    if agent.get("isAlive") == False and aliveCounter == 3:
        agentData = {"coordX": agent.get("coordX"), "coordY": agent.get("coordY"), "isAlive": False,
                     "newIsAlive": True}
    elif agent.get("isAlive") == True and (aliveCounter == 2 or aliveCounter == 3):
        agentData = {"coordX": agent.get("coordX"), "coordY": agent.get("coordY"), "isAlive": True,
                     "newIsAlive": True}
    elif agent.get("isAlive") == True and not (aliveCounter == 2 or aliveCounter == 3):
        agentData = {"coordX": agent.get("coordX"), "coordY": agent.get("coordY"), "isAlive": True,
                     "newIsAlive": False}
    else:
        agentData = {"coordX": agent.get("coordX"), "coordY": agent.get("coordY"), "isAlive": agent.get("isAlive"),
                     "newIsAlive": agent.get("isAlive")}
    r2 = requests.post(update_url, data=json.dumps(agentData), headers=headers)
