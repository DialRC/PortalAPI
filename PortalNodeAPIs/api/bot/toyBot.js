'use strict';

var example_return = {
    sessionID: "USR_001",
    sys: "This is a toy example for you.",
    terminal: false,
    timeStamp: "yyyy-MM-dd'T'HH-mm-ss.SSS"
};

exports.init = function(req, res) {
    // what you get from portal
    console.log("Portal just initialized a new session.");
    console.log("sessionID is: " + req.body.sessionID);
    console.log("timeStamp is: " + req.body.timeStamp);

    // what you send back
    example_return.sessionID = req.body.sessionID;
    example_return.sys = "Hello! (Portal just initialized a new session.)";

    res.json(example_return);
};


exports.next = function(req, res) {
    // what you get from portal
    console.log("Portal just send a message from user: " + req.body.text);
    console.log("sessionID is: " + req.body.sessionID);
    console.log("timeStamp is: " + req.body.timeStamp);

    // what you send back
    example_return.sessionID = req.body.sessionID;
    example_return.sys = "Sorry, I am just a toy!"; 

    res.json(example_return);
};


exports.end = function(req, res) {
    // what you get from portal
    console.log("Portal will end the current session: " + req.body.sessionID);
    console.log("sessionID is: " + req.body.sessionID);
    console.log("timeStamp is: " + req.body.timeStamp);

    // what you send back
    example_return.sessionID = req.body.sessionID;
    example_return.sys = "Goodbye!"; 
    example_return.terminal = true;

    res.json(example_return);
};