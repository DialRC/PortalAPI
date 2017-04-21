# DialportAPI
A zoo of API wrapper for connecting to DialPort 

## Protocol:
### Initialize a New Session
POST http://localhost:port/init

```javascript
{
    sessionID: "USR_1234",
    timeStamp: "yyyy-MM-dd'T'HH-mm-ss.SSS"
}
```

### Get the Next Response of a Ongoing Session
POST http://locahost:port/next

```javascript
{
    sessionID: "USR_1234",
    text: "I guess the answer is APPLE", 
    asrConf: 0.9,
    timeStamp: "yyyy-MM-dd'T'HH-mm-ss.SSS"
}
```
There is also a specical symbol to deal with time out. The message will
still be sent via port/next

```javascript
{
    sessionID: "USR_1234",
    text: "TIME_OUT", 
    asrConf: 1.0,
    timeStamp: "yyyy-MM-dd'T'HH-mm-ss.SSS"
}
```

### Expected Return Format

All the POST requests will have the same return JSON format. 
```javascript
{
    sessionID: "USR_1234",
    sys: "This word starts with A",
    roundNumber: 3,
    timer: 140,
    terminal: False,
    roundScore: 4,
    totalScore: 10,
    version: "1.0-xxx",
    timeStamp: "yyyy-MM-dd'T'HH-mm-ss.SSS"
}
```
If non-verbal output is also needed. Please add the non-verbal features into the JSON.

### Timezone.
For easier synchronization with DialPort server logging system. Use UTC-4 timezone for all time stamps. 


### Example Framework
Java: [JAVA Spark Framework](https://github.com/perwendel/spark)


Python: [Flask](http://flask.pocoo.org)
