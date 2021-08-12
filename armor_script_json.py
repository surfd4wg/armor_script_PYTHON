#!/usr/bin/python3
# Authors:
#  Craig Ellrod, Joshua Seither
#
# Grab your API Key Id and Secret Key from the Armor Management Portal
# and plug them in below.
# This script simply calls the armor API and outputs the unformatted resposne to a .txt file, also
# it outputs the pretty json to a .json file.
# To call a different API endpoint, replace the request_path='API-ENDPOINT'
# Usage: (Python3)
# ./armor_script_json.py
#
import base64
import hashlib
import hmac
import requests
import sys
import time
import urllib.parse
import uuid
import json

ENCODING = 'utf-8'

def get_auth_header_value(api_key,
                          api_key_secret,
                          request_method,
                          request_path,
                          serialized_request_body):
  timestamp = int(time.time())
  nonce = uuid.uuid4()
  # TODO: check if method is not GET and hash/base64 serializedRequestBody
  # for GET empty string is enough
  request_body = '' if serialized_request_body is None else serialized_request_body
  request_data = f'{api_key}{request_method}{request_path}{nonce}{timestamp}{request_body}'
  hash = hmac.new(bytes(api_key_secret, ENCODING), bytes(request_data, ENCODING), hashlib.sha512)
  signature = base64.standard_b64encode(hash.digest()).decode(ENCODING)
  print ('signature', signature)

  return f'ARMOR-PSK {api_key}:{signature}:{nonce}:{timestamp}'

def execute_get(api_key,
                api_secret_key,
                base_url,
                request_path):
  request_method = 'GET'
  auth_header_value = get_auth_header_value(api_key,
                                            api_secret_key,
                                            request_method,
                                            request_path,
                                            '')
  headers = {
    'Authorization': auth_header_value,
    'Content-Type': 'application-json'
  }
  print ('auth_header_value', auth_header_value)
  url = urllib.parse.urljoin(base_url, request_path)
  response = requests.get(url, headers=headers)
  #print(response.text)
  #print(response.json)

  # Build output filename, to later use as input into 'jq'
  string=request_path
  endPointOutputFilename=string.replace("/", "_")+".txt"
  endPointOutputFilenameJson=string.replace("/", "_")+".json"
  print ('Output Filename: ', endPointOutputFilename)
  print ('Output Filename Pretty Json: ', endPointOutputFilenameJson)

  # Write the output to .txt file
  open(endPointOutputFilename, 'wb').write(response.content)

  # Format the output into pretty json, output to pretty .json file
  with open(endPointOutputFilename, 'r') as json_file:
    json_object = json.load(json_file)

  json_output=(json.dumps(json_object, indent=2, separators=(',', ': '), sort_keys=True))
  #print('json_output: ', json_output)
  open(endPointOutputFilenameJson, 'wb').write(bytes(json_output, encoding='utf-8'))

if __name__ == '__main__':
  api_key = "API-KEY-ID"
  api_secret_key = "SECRET-KEY"

  # Make sure the url does not end with a slash
  base_url = 'https://api.armor.com'

  # Make sure the path begins with a slash
  request_path = '/tickets/list'
  execute_get(api_key, api_secret_key, base_url, request_path)


