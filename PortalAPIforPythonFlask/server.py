'''
    Author: Kyusong Lee
    email: kyusongl@cs.cmu.edu
    Date created: 09/21/2017
    Date last modified: 09/21/201
    Description: An Example code for DialPort Connection
    Python Version: 2.7
'''

from flask import Flask, request, jsonify
app = Flask(__name__)
from datetime import datetime
from RemoteAgent import * # Import your code

usrStacks = {}
date_format = "%Y-%m-%d'T'%H%-%M-%S.SSS"
@app.route('/<uuid>', methods=['GET', 'POST'])
def add_message(uuid):
    if uuid == "init":
        content = request.json
        sessionID = content["sessionID"]
        usrStacks[sessionID] = API()
        Instance = {}
        Instance["sessionID"] = sessionID # DialPort will send sessionID. 
        Instance["version"] = "0.1" # Please provide your system version. 
        Instance["terminal"] = False
        if "timeStamp" in content:
            Instance["timeStamp"] = content["timeStamp"]
        else:
            Instance["timeStamp"] = datetime.now().isoformat() 
        Instance["sys"] = "Welcome to Mybot... " # Introduction Message
        Instance["imageurl"] = "https://skylar.speech.cs.cmu.edu/image/movie.jpg" # Put an image url to show on the screen."
        return jsonify(Instance)

    if uuid == "next":
        content = request.json
        sessionID = content["sessionID"]
        text =  content["text"]
        Instance = {}
        if "timeStamp" in content:
            Instance["timeStamp"] = content["timeStamp"]
        else:
            Instance["timeStamp"] = datetime.now().isoformat() 
        asrConf = content["asrConf"] 
        Instance["sessionID"] = sessionID
        Instance["version"] = "0.1"
        response = usrStacks[sessionID].GetResponse(text)

        if response["slu"]["act"] == "exit":
            Instance["sys"] = "Goodbye. See you later"
            Instance["terminal"] = True # At the end of the dialog, please send us True
            del usrStacks[sessionID]
        else:
            Instance["imageurl"] = response["imageurl"]
            Instance["terminal"] = False
            Instance["sys"] = response["sys"]
        return jsonify(Instance)

    if uuid == "test":
        return jsonify({"check":"fine"})

if __name__ == '__main__':
    app.run(host= '0.0.0.0',port= 9990, debug=True)
