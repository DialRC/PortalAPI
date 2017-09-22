# Portal Tutorial

## Introduction

## How Portal Works?

## Example

## API Documentations:
### Initialize a New Session
**Create a new session**

Start a new session with your dialog system. If successful, the server will return an JSON containing the session ID.

**URL**

    /init

**Method:**

   `POST`
  
**Body Data**

    { sessionID: USR_1234,
      timeStamp: "yyyy-MM-dd'T'HH-mm-ss.SSS"
    }
     
**Success Response (200):** 
	
	{
	  "sessionID": "USR_1234",
	  "sys": "This word starts with A",
	  "version": "1.0-xxx",
	  "timeStamp": "yyyy-MM-dd'T'HH-mm-ss.SSS",
	  "terminal": false
	}
```

### Get the Next Response of a Ongoing Session
POST http://locahost:[YOUR_SYSTEM_NAME]/next

```javascript
{
    sessionID: "USR_1234",
    text: "I guess the answer is APPLE", 
    asrConf: 0.9,
    timeStamp: "yyyy-MM-dd'T'HH-mm-ss.SSS"
}
```

### Expected Return Format

All the POST requests will have the same return JSON format. 
```javascript
{
    sessionID: "USR_1234",
    sys: "This word starts with A",
    version: "1.0-xxx",
    timeStamp: "yyyy-MM-dd'T'HH-mm-ss.SSS"，
    terminal: False,
}
```
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
