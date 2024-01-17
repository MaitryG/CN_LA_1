# HTTPC

httpc is a curl-like command line application which is executable on the terminal/command-line. Its main function is to query to HTTP Servers and get response to the user. It can query server for files, content, media, HTML files, etc. 
## Installation

As httpc is a command-like application, we need to make the python file executable. In order to do that, follow the below steps depending on the type of machine that you use:

### For Linux/macOS:

1.) Make main.py executable:

First, ensure your Python script has the execute permission. You can use the chmod command in the terminal to add the execute permission to your Python file:

```bash
chmod +x main.py 
```
2.) Create a shell script: 


Create a new shell script named ’httpc’ in a directory that is included in your system's ***PATH***. Go to ***/usr/local/bin*** directory. Enter the following command to create a shell script: 
```bash
vim httpc
````
3.) Edit the file:

Then write the following script in the httpc file. Write the full path in your system to the main.py file. Save the file and quit.
```bash
#!/bin/bash
python3 /home/maitry/PyCharmProjects/CN_LA_1/main.py "$@"
```

4.) Make the shell script executable:

Enter the following command:
```bash
chmod +x /usr/local/bin/httpc
```
Now, you can run **httpc** in the terminal with all the options.

### For Windows:
1.) Create a batch file:

Create a new batch file (e.g., httpc.bat) in a directory included in your system's PATH. Open the batch file in a text editor and add the following line:
```bash
@echo off
python C:\path\to\main.py %*
```
Replace C:\path\to\main.py with the actual path to your Python script.

2.) Add the batch file to the system's PATH:

Ensure the directory containing your batch file is included in the system's PATH
environment variable. This allows you to run the batch file from any command prompt window.

After following these steps, you can use httpc in the terminal or command prompt to execute your Python script.

## Usage
NOTE: httpbin.org is an echo server so it will just echo everything you send to it. You can use the application with other HTTP Servers as well. 

1.) GET request with verbose and headers
```bash
httpc get -v --headers Content-Type:application/json ‘http://httpbin.org/get?course=networking&assignment=1'
```
2.) Basic help command
```bash
httpc --help
```
3.) Help about GET
```bash
httpc get --help
```
4.) Help about POST 
```bash
httpc post --help
```
5.) Post data to the Server
```bash
httpc post --data ‘{“Assignment”:1}’ http://httpbin.org/post
```
6.) Post with headers
```bash
httpc post --headers Content-Type:application/json --data '{Assignment: 1}' http://httpbin.org/post
```
