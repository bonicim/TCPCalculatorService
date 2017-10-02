
#Networking programming assignment #1
## Instructions on how to use Calculator service
### Assumptions: 
* Client must enter expressions in infix form (e.g. 2+2/486)
* Client cannot give expression for dividing by 0 (e.g., 23/0)
* Client cannot put spaces, quotation marks, or any punctuation marks in expressions
* The only operators allowed are '+', '-', '*', and '/'. Parathesis '()' are not allowed.
* Any violation of these rules will result in an error and the client will simply 'hang'
* Client session terminates once results are received; thus you must start a new client session if you want to submit another request

## Instructions
1. On your machine, open two terminal/command line windows.
2. On the left terminal window, navigate to the file 'tcp-server.py'
3. Enter the command: 'python3 tcp-server.py'
4. On the right terminal window, navigate to the file 'tcp-client.py'
5. Enter the command: 'python3 tcp-client.py'
6. Follow the instructions from the client text interface and await the response from the server. 
