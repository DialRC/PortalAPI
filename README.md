# DialPort Portal Tutorial

* [Introduction](#introduction)
* [How the portal Works](#how-the-portal-works)
* [Development Cycle](#development-cycle)
* [API Documentations:](#api-documentations)
  * [1\. Create a new session](#1-create-a-new-session)
  * [2\. Get your system's next response](#2-get-your-systems-next-response)
  * [3\. Terminate a session with your system](#3-terminate-a-session-with-your-system)
  * [Extra Parameters](#extra-parameters)
  * [Timezone](#timezone)
  * [Example Server Templates](#example-server-templates)
* [Interested in working with us?](#interested-in-working-with-us)


## Introduction
In order to make testing easier and more automated, a framework for connecting to a crowdsourcing entity such as (but not only) Amazon Mechanical Turk (AMT) and for rapidly creating and deploying tasks.
Our inspiration comes from TestVox (Parlikar 2012), a tool that addresses speech synthesis evaluation experiments. TestVox enables any developer to quickly upload data in a standard format and then deploy it on AMT or some other crowd sourcing site, or to a controlled set of developer-selected workers and get results easily and rapidly. In our experience, there are often a small set of standardized test scenarios (templates) that cover a large portion of the dialog tasks that are run on AMT. When we make those scenarios easy to create, testing is faster, and less burdensome. For some who are new to the area, the use of these scenarios guides them to accepted testing structures that they may not have been aware of.
While developing a dialog system, researchers often need to run a small set of standardized tests. These will also be available. At the outset, the Task Creation Toolkit will use standard templates that are easy to flesh out. Later, when the toolkit is finished, the community will be invited to add more.
The toolkit will include tests that are both interactive and non-interactive. The simplest tests, non-interactive tests, present some part of a dialog for worker evaluation. We want these to be as easy as possible to run.  Given a dialog log format, the experiment designer selects the set of turns and the context they wish to present, perhaps with optional follow up replies. Then a website automatically becomes available and, given a userid, presents the examples in randomized order and collects the necessary statistics. Thus, for example, if Jane wants to use a well-defined measure, such as acceptability of system utterances, she could quickly get 50 workers to see 20 different examples in randomized order and collect their agreement on the acceptability of these utterances. DialCrowd will simply make it easy to run it as a web app for direct use on a crowdsourcing site.
Interactive tests ask the worker to actually interact with a dialog system. There may be scenario instructions, and/or constraints on the worker’s interactions. There will probably be different conditions for each dialog class. Again the Toolkit will make it easy to run 50 users through 10 scenarios with 3 different conditions by creating the web front end, collecting the data, and keeping track of which worker has done what. Beyond these two types of tests, we will eventually find other types that enable more novel studies. They will be added as needed.
The Toolkit will aid in other aspects of running tasks such as, in relevant cases, remembering to post a consent form for explicit permission to use the data. We will ensure that the results are collected ethically and can be made available to the community with as few restrictions as possible that do not compromise a worker’s privacy. We will also suggest correct levels of payment, aided by the groundbreaking work of Gao et al 2015.


## How the dialCrowd Works
![Image](images/overview.png)

**Figure 1**

Figure 1 shows an overview about the relations between the Portal and agents. Agents here are defined as any remote dailog systems that have joined Portal. 

The Portal is responsible for facing the users via web or mobile interfaces. It will also provide the following services to all the agents:

- ASR/TTS
- Meta Dialog Management
- Domain Tracking
- Context Keeping
- Agent Selection

As for an agent, it has to implement an HTTP API server that supports 3 Portal APIs /init, /next, /end. (defined below). 

Generally speaking, the Portal and an agent will interact as follows:

1. The Portal will first interact with a user to find out what the user is interested in (*domain tracking*).
2. Portal will try to select an remote agent that matches the user's needs the best (*agent selection*).
3. Portal then starts a new remote session with the selected agent via (*/init*).
4. Portal will then pass every user utterances to the selected agent via (*/next*). The user is effectively talking to the selected agent.
5. After the selected agent decides to finish the conversation, the control is back to the Portal and we go back to *Step 1*.
6. Rarely, the remote agent does not perform well. Portal will end the session via (*/end*) and go back to *Step 1*. 

The above transitions can be compactly represented in the finite-state machine in Figure 2.

![Image](images/fsm.png)

**Figure 2**

## Development Cycle

![Image](images/flow.png)

**Figure 3**

Figure 3 shows the steps that you need to take to become a part of DialPort Portal.

## API Documentations:
For a remote agent, all it needs to do is to implement the following 3 API interfaces. They are: 

1. /init
2. /next
3. /end

Very simple!

### 1. Create a new session ###

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

### 2. Get your system's next response

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

### 3. Terminate a session with your system ###

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
	
### Extra Parameters
We are open to any system expecting extra input parameters or returning extra parameters for better interaction purpose. 
Here are some example extra parameters:

Input: initial domain that user is looking for, user profile and etc.

Output: nonverbal behavior of the agent. Multimedia outputs (photo links, meta information and etc.)

### Timezone
For easier synchronization with the DialPort server logging system. Use UTC-4 timezone for all time stamps. 


### Example Server Templates
We provide server templates implemented in 3 popular frameworks for your convenience. 

Java: [JAVA Spark Framework](https://github.com/DialRC/RestMrClue)

Python: [Flask](https://github.com/DialRC/PortalAPI/tree/master/PortalAPIforPythonFlask)

Javascript: [Nodejs](https://github.com/DialRC/PortalAPI/tree/master/PortalNodeAPIs) 

## Interested in working with us?
We are happy to hear that you'd like to connect to DialPort. 

**Please read the overall process of connecting to DialPort:** 

1) Please email Dr. Maxine Eskenazi (max at cs dot cmu dot edu) and include the following description of your system :

	(An Example)
	> Organization: Carnegie Mellon University
	>
	> Contact person in your organization: Kyusong Lee (email: kyusonglee at gmail dot com)
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
