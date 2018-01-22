# -*- coding: utf-8 -*-
# Author: Tiancheng Zhao
# Date: 1/22/18

import requests
import json
import uuid
import datetime

AGENT_URL = "http://localhost:3000"
KEY_WORD = "hello world"

def run_server():
    print("Welcome to DialPortal Mock Portal. \nThis program simulates the process"
          "a user talking to the Portal and the Portal redirect the user to your agent.")
    print("Simulation starting now. Type EXIT to quit.\n")
    print("Hi, I am the Portal from. What can I do for you?")
    state = "in_portal"
    sess_id = None

    while True:
        usr_input = raw_input("You can say '{}' to activate your system\n".format(KEY_WORD))

        if usr_input == 'EXIT':
            break

        try:
            if state == 'in_portal':
                if usr_input.strip() == KEY_WORD:
                    state = "in_agent"
                    sess_id = str(uuid.uuid4())
                    # start a new session with your agent
                    body = {'sessionID': sess_id,
                            'timeStamp':datetime.datetime.now().__str__()}
                    resp = requests.post(AGENT_URL + '/init', data=json.dumps(body))
                    resp = json.loads(resp.text)
                    print("Agent: {}".format(resp['sys']))

                    # if the remote agent just finish 1 turn, stop
                    if resp['terminal']:
                        state = 'in_portal'
            else:
                body = {'sessionID': sess_id,
                        'timeStamp': datetime.datetime.now().__str__(),
                        'text': usr_input,
                        'asrConf': 0.9}

                resp = requests.post(AGENT_URL + '/next', data=json.dumps(body))
                resp = json.loads(resp.text)
                print("Agent: {}".format(resp['sys']))

                # if the remote agent just finish 1 turn, stop
                if resp['terminal']:
                    state = 'in_portal'
                    sess_id = None
        except Exception as e:
            print(e)
            print("!!You agent is not working yet. Please debug and try agin.")


if __name__ == "__main__":
    run_server()