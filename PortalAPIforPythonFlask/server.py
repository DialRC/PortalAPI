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
from RemoteAgent import * # Import your bot

usrStacks = {}
date_format = "%Y-%m-%d'T'%H%-%M-%S.SSS"
@app.route('/<uuid>', methods=['GET', 'POST'])
def add_message(uuid):
    if uuid == "init": #Create a new session
        content = request.json
        #A message from DialPort: sessionID, timeStamp
        sessionID = content["sessionID"]
        timeStamp = content["timeStamp"]
        
        # Assign an instance to Dictionary 
        usrStacks[sessionID] = API() 

        #A message to DialPort: sessionID, version, terminal, sys, and imageurl
        Output = {}
        Output["sessionID"] = sessionID # DialPort will send sessionID. 
        Output["version"] = "0.1" # Please provide your system version. 
        Output["terminal"] = False
        Output["timeStamp"] = datetime.now().isoformat() 
        Output["sys"] = "Welcome to Mybot... " # Introduction Message
        Output["imageurl"] = "https://skylar.speech.cs.cmu.edu/image/movie.jpg" # Put an image url to show on the screen."
        return jsonify(Output)

    if uuid == "next": #Get your system's next response
        content = request.json
        #A message from DialPort: sessionID, text (an user input), asrConf, timeStamp
        sessionID = content["sessionID"]
        text =  content["text"]
        asrConf = content["asrConf"] 
        timeStamp = content["timeStamp"]
        
        # A reponse from your bot
        response = usrStacks[sessionID].GetResponse(text)
        
        # A message to DialPort: sessionID, version, sys (system utterance), terminal (true if the end of the dialog), imageurl
        Output = {}
        Output["sessionID"] = sessionID
        Output["timeStamp"] = datetime.now().isoformat() 
        Output["version"] = "0.1"
        if response["slu"]["act"] == "exit":
            Output["sys"] = "Goodbye. See you later"
            Output["terminal"] = True # At the end of the dialog, please send us True
            del usrStacks[sessionID]
        else:
            Output["imageurl"] = response["imageurl"]
            Output["terminal"] = False
            Output["sys"] = response["sys"]
        return jsonify(Output)
    
    if uuid == "end":  #Terminate a session with your system
        content = request.json
        #A message from DialPort: sessionID, timeStamp
        sessionID = content["sessionID"]
        timeStamp = content["timeStamp"]
        
        # A message to DialPort: sessionID, version, sys (system utterance), terminal (true if the end of the dialog)
        Output = {}
        Output["sessionID"] = sessionID
        Output["timeStamp"] = datetime.now().isoformat() 
        Output["version"] = "0.1"
        Output["sys"] = "Goodbye. See you later"
        Output["terminal"] = True # At the end of the dialog, please send us True
        del usrStacks[sessionID]
        return jsonify(Output)

if __name__ == '__main__':
    app.run(host= '0.0.0.0',port= 3000, debug=True)
