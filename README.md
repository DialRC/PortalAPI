# DialPort Portal Tutorial

## Introduction
The advent of Siri and other agents has generated interest in spoken dialog research, sparking the imagination of many and leading them to believe in the usefulness of speaking to intelligent agents. The research community can profit from this interest to gather much needed real user data by joining a service for the general public. The service will be the front end of many different academic dialog systems in order to serve more diverse requests. The data gathered from such a service can make dialog systems more robust and be used to carry out comparative studies. Industry has already collected large data sets and sometimes retains pools of real users. They are viewed as strategic competitive resources and so not shared with the research community. Much fundamental research remains to be done, such as signal processing in noisy conditions' recognition of groups of difficult users (like the elderly and non-natives), management of complex dialogs (such as multi party meetings, negotiations, and multimodal interaction), and the automatic use of meta linguistic information such as prosody. It is difficult for any one group to collect a significant amount of real user data. The users must be found and their interest maintained while the interface must be kept up to date. By having one data-gathering portal that all dialog systems can be connected to, the task for each participating site is easier and the portal is more interesting to potential users. Potential users find a variety of interesting applications and can choose which ones fulfill their needs at any given time. Also, with one central site (the portal), only the researchers maintaining the portal itself taken on the task of attracting users. The DialPort portal was created for this purpose.

## How the portal Works

## Example

## API Documentations:
**Create a new session**

Start a new session with your dialog system. If successful, the server will return an JSON containing the session ID.

**URL**

    /init

**Method:**

   `POST`
  
**Body Data**

    { "sessionID": "USR_1234",
      "timeStamp": "yyyy-MM-dd'T'HH-mm-ss.SSS"
    }
     
**Success Response (200):** 
	
	{
	  "sessionID": "USR_1234",
	  "sys": "This word starts with A",
	  "version": "1.0-xxx",
	  "timeStamp": "yyyy-MM-dd'T'HH-mm-ss.SSS",
	  "terminal": false
	}

### Get the Next Response of an Ongoing Session
**Get your system next response**

For an ongoing session, the portal will use this API to obtain the next system response from your dialog system.

**URL**

    /next

**Method:**

   `POST`
  
**Body Data**

	{
	    "sessionID": "USR_1234",
	    "text": "I guess the answer is APPLE", 
	    "asrConf": 0.9,
	    "timeStamp": "yyyy-MM-dd'T'HH-mm-ss.SSS"
	}
	     
**Success Response (200):** 
	
	{
	  "sessionID": "USR_1234",
	  "sys": "This word starts with A",
	  "version": "1.0-xxx",
	  "timeStamp": "yyyy-MM-dd'T'HH-mm-ss.SSS",
	  "terminal": false
	}

**Terminate a session with your system**

The portal sometimes (very rarely) wants to terminate an ongoing session with your dialog system (e.g. due to a lost connection, conversation failure etc.)

**URL**

    /end

**Method:**

   `POST`
  
**Body Data**

	{
	    "sessionID": "USR_1234",
	    "timeStamp": "yyyy-MM-dd'T'HH-mm-ss.SSS"
	}
	     
**Success Response (200):** 
	
	{
	  "sessionID": "USR_1234",
	  "sys": "Goodbye",
	  "version": "1.0-xxx",
	  "timeStamp": "yyyy-MM-dd'T'HH-mm-ss.SSS",
	  "terminal": true
	}
	
### Extra Parameters:
We are open to any system expecting extra input parameters or returning extra parameters for better interaction purpose. 
Here are some example extra parameters:

Input: initial domain that user is looking for, user profile and etc.

Output: nonverbal behavior of the agent. Multimedia outputs (photo links, meta information and etc.)

### Timezone.
For easier synchronization with the DialPort server logging system. Use UTC-4 timezone for all time stamps. 


### Example Framework
Java: [JAVA Spark Framework](https://github.com/perwendel/spark)

Python: [Flask](http://flask.pocoo.org)

Javascript: [Nodejs]() 

## Interested in working with us?
We are happy to hear that you'd like to connect to DialPort. 

**Please read the overall process of connecting to DialPort:** 

1) Please email Dr. Maxine Eskenazi (max@cs.cmu.edu) and include the following description of your system :

	(An Example)
	> Organization: Carnegie Mellon University
	>
	> Contact person in your organization: Kyusong Lee (email: kyusonglee@gmail.com)
	>
	> Domain (for example, weather, restaurants) : open domain
	>
	> Language: English
	>
	> Name of your system: Qubot
	>
	> Description: Qubot is a chat-oriented dialog system. ..... 
	>
	> Interface (Describe the interface you presently use - microphone, camera, avatar, 3D, etc.): Just a text input using keyboard.
	>
	> Keywords: chatbot, question answering, 
	>
	> Examples of utterances that your system would handle: who is the president of United States?, what is the highest mountain in the world?..,
	>
	> Schedule (when can we try your system, when could you try a connection): We would like to contribute the system in late June. Currently our system is being tested internally. 

2) When we accept to have you join the Portal, we will give the detailed explanation and some sample code for DialPort integration

3) First the system will connect to the Dev version of DialPort and be tested internally by both the DialPort team and your group. 

4) When the system is robust enough, the system will be promoted to the master version.

5) In order to be promoted to the Master version, you must demonstrate that you have IRB permission from your institution. To do this, you should contact Dr. Eskenazi and she will give you the CMU IRB application as well as the present consent form. You are repsonsible for gathering, maintaining and distributing the data corresponding to all of the dialog that users have with your system.


If you have any questions, please feel free to contact us.
