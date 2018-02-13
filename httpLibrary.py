'''
author: Yang An 27878699
'''
#########################
#    http Library       #
#########################
from socket import *
import argparse
from urllib.parse import urlparse
import sys

'''
:param host: host associate with url
:param port: port
:param request: request string from get or post method
:param verbose: boolean value enables a verbose output from the command-line
:param output: Bonous write body of the HTTP Request with the data from a given file
'''
def processRequest(host, port, request, verbose, output):
   
  print("Request:")
  print(request)
  
  # create TCP socket
  clientSocket = socket(AF_INET, SOCK_STREAM)
  # connect
  clientSocket.connect((host,port))
  # send the request
  clientSocket.sendall(request.encode("utf-8"))
  
  # response
  response = clientSocket.recv(1024).decode("utf-8")
  responseArr = response.split('\r\n\r\n')
  responseHeaders = responseArr[0]
  responseData = responseArr[1]

  print("Output:")

  ########### -o argument ##############
  if output is not None:
    f = open(output, 'w')
    f.write(response)
    f.close()
  
  #If the request is a NOT verbose type
  if not verbose:
    print(responseData)
  #If the request is a NOT verbose type
  else:      
    print(response)
  clientSocket.close()

  ############Redirection################
  # if the client receives a redirection code
  statusLine = responseHeaders.split('\r\n')[0]
  statusCode = int(statusLine.split(' ')[1])
  # print(statusCode)
  # if status code is 3xx return new location
  if statusCode>=300 and statusCode<400:
    newLocation = ''
    for header in responseHeaders.split('\r\n'):
      if header.startswith('Location:'):
        newLocation = header[10:]
        print("New Location: ", newLocation)
        return newLocation
  

######GET operation########
'''
:param url: url
:param headers: {key:value} multiple headers through input
:param verbose: boolean value enables a verbose output from the command-line
:param output: Bonous write body of the HTTP Request with the data from a given file
'''
def get(url,headers,verbose,output):

  # prepare request
  # parse url get hostname, path and query
  host = urlparse(url).hostname
  path = urlparse(url).path
  query = urlparse(url).query
  port = 80
  
  # build http request method, query, host
  request = "GET " + path + "?" + query + " HTTP/1.1\r\nHost: " + host + "\r\n"
  
  # handle multiple headers
  if headers is not None:
    for key,value in headers.items():
      if key is not 'Host':
        request = request + key + ": " + value +"\r\n"
  
  request = request + "\r\n\r\n"

  location = processRequest(host, port, request, verbose, output)
 
 ############Redirection################
  if location is not None:
    redirectTo = input("Do you want to follow the redirection link? [y/n]: ")
    if redirectTo != 'n' :
      get(location, headers, verbose,output)


#########POST operation################
'''
:param url: url
:param headers: {key:value} multiple headers through input
:param verbose: boolean value enables a verbose output from the command-line
:param data: in-line data
:param file: body of the HTTP Request with the data from a given file
:param output: Bonous write body of the HTTP Request with the data from a given file
'''
def post(url,headers,verbose,data,file,output):
  
  # parse url get hostname, path and query
  host = urlparse(url).hostname
  path = urlparse(url).path
  port = 80 
 
  # build http request method and host
  request = "POST " + path + " HTTP/1.1\r\nHost: " + host + "\r\n"

  # handle multiple headers
  if headers is not None:
    for key,value in headers.items():
      if key is not 'Host':
        request = request + key + ": " + value +"\r\n"

  # request body
  body = ''
  # inline data
  if data is not None:
    body = body + data
  # file
  elif file is not None:
    with open(file,'r') as f:
      for line in f:
        body = body + line.replace('\n','') +'&'

  # complete request
  request = request + "Content-Length: " + str(len(body)) + "\r\n\r\n"
  request = request + body +'\r\n'

  location = processRequest(host, port, request, verbose, output)

  ############Redirection################
  if location is not None:
    redirectTo = input("Do you want to follow the redirection link? [y/n]: ")
    if redirectTo != 'n' :
      post(location, headers, verbose, data, file, output)

