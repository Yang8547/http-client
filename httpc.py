'''
author: Yang An 27878699
'''

import argparse
from httpLibrary import *
 
#########################
#cURL-like Command Line #
#########################

parser = argparse.ArgumentParser(prog="httpc", 
                                 description='''httpc is a curl-like application but supports HTTP protocol only''',
                                 usage='%(prog)s command [arguments]:',
                                 epilog="httpc [command] -h for more information about a command")
subParsers = parser.add_subparsers(dest="subparser_name")

# -v and -H are common arguments associate with parent parser
parentParser = argparse.ArgumentParser(add_help=False)
parentParser.add_argument('-v', help='Prints the detail of the response such as protocol,status, and headers.', dest="isVerbose", action="store_const", const=True, default=False,)
parentParser.add_argument('-H', help="key:value Associates headers to HTTP Request with the format\'key:value\'.", dest="headers", action="append",)
parentParser.add_argument('URL', action="store", help="URL for the Http request. put URL in double quotation marks \"\" ",type=str)
parentParser.add_argument('-o', action="store", help='write the body of the response to the specified file instead of the console.', type=str)

# get command
getParser = subParsers.add_parser('get', parents=[parentParser], help='executes a HTTP GET request for a given URL.')

# post command
postParser = subParsers.add_parser('post', parents=[parentParser], epilog="Either [-d] or [-f] can be used but not both.",help='executes a HTTP POST request for a given URL with inline data or from file.')

# Either [-d] or [-f] can be used but not both, these two arguments associate with post
bodyGroup = postParser.add_mutually_exclusive_group()
bodyGroup.add_argument('-d', help='string  Associates an inline data to the body HTTP POST request. put string in double quotation marks \" \" ', type=str)
bodyGroup.add_argument('-f', help='file  Associates the content of a file to the body HTTP POST request.', type=str)


args = parser.parse_args()
# print(args)

# handle headers [':',':'], put all headers in the headers dictionary
headers = {}
if args.headers is not None:
  for header in args.headers:
    splitHeader = header.split(':')
    headerKey = splitHeader[0]
    headerValue = splitHeader[1]
    headers[headerKey] = headerValue

output = args.o

# execute post command
if args.subparser_name =='post':
  data = args.d
  file = args.f
  post(args.URL, headers, args.isVerbose, data, file, output)
# execute get command args.subparser_name == 'get' 
else:
  get(args.URL, headers, args.isVerbose, output)


