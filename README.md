# Portal Tutorial

## Introduction
The advent of Siri and other agents has generated interest in spoken dialog research, sparking the imagination of many and leading them to believe in the usefulness of speaking to intelligent agents. The research community can profit from this interest to gather much needed real user data by joining a service for the general public. The service will be the front end of many different academic dialog systems in order to serve more diverse requests. The data gathered from such a service can make dialog systems more robust and be used to carry out comparative studies. Industry has already collected large data sets and sometimes retains pools of real users. They are viewed as strategic competitive resources and so not shared with the research community. Much fundamental research remains to be done, such as signal processing in noisy conditions' recognition of groups of difficult users (like the elderly and non-natives), management of complex dialogs (such as multi party meetings, negotiations, and multimodal interaction), and the automatic use of meta linguistic information such as prosody. It is difficult for any one group to collect a significant amount of real user data. The users must be found and their interest maintained while the interface must be kept up to date. By having one data-gathering portal that all dialog systems can be connected to, the task for each participating site is easier and the portal is more interesting to potential users. Potential users find a variety of interesting applications and can choose which ones fulfill their needs at any given time. Also, with one central site (the portal), only the researchers maintaining the portal itself taken on the task of attracting users. The DialPort portal was created for this purpose.

## How Portal Works?

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

### Get the Next Response of a Ongoing Session
**Get your system next response**

For a ongoing session, Portal will use this API to obtain the next system response from you dialog systems.

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

Portal sometimes (very rarely) wants to terminate an ongoing session with your dialog system (e.g. due to loss connection, conversation failure etc.)

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
We welcome any system to expect extra input parameters or return extra parameters for better interaction purpose. 
Here are some example extra parameters:

Input: initial domain that user is looking for, user profile and etc.

Output: nonverbal behavior of the agent. Multimedia outputs (photo links, meta information and etc.)

### Timezone.
For easier synchronization with DialPort server logging system. Use UTC-4 timezone for all time stamps. 


### Example Framework
Java: [JAVA Spark Framework](https://github.com/perwendel/spark)

Python: [Flask](http://flask.pocoo.org)

Javascript: [Nodejs]() 
