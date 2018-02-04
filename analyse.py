from __future__ import print_function
import time
import requests
import cv2
import operator
import numpy as np
import matplotlib.patches as patches
import json
import pprint
import matplotlib.pyplot as plt
import captions as captionsFile

#from flask import Flask
#app = Flask(__name__)

#@app.route("/")

# Variables
_region = 'westcentralus'  # Here you enter the region of your subscription
_url = 'https://{}.api.cognitive.microsoft.com/vision/v1.0/analyze'.format(_region)
# _url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1/analyses'
_key = 'b4613b2c27174a32adda156e49176434'  # Here you have to paste your primary key
_maxNumRetries = 10


def processRequest(json, data, headers, params):
    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request('post', _url, json=json, data=data, headers=headers, params=params)

        if response.status_code == 429:

            print("Message: %s" % (response.json()))

            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying!')
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    result = response.json() if response.content else None
                elif 'image' in response.headers['content-type'].lower():
                    result = response.content
        else:
            print("Error code: %d" % (response.status_code))
            print("Message: %s" % (response.json()))

        break

    return result


def renderResultOnImage(result, img):
    """Display the obtained results onto the input image"""

    R = int(result['color']['accentColor'][:2], 16)
    G = int(result['color']['accentColor'][2:4], 16)
    B = int(result['color']['accentColor'][4:], 16)

    cv2.rectangle(img, (0, 0), (img.shape[1], img.shape[0]), color=(R, G, B), thickness=25)

    if 'categories' in result:
        categoryName = sorted(result['categories'], key=lambda x: x['score'])[0]['name']
        cv2.putText(img, categoryName, (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)

def getMetadata(result):
    captions = result["description"]["captions"]
    tags = result["description"]["tags"]
    return [captions, tags]

def displayImage(url):
    # Load the original image, fetched from the URL
    arr = np.asarray(bytearray(requests.get(url).content), dtype=np.uint8)
    img = cv2.cvtColor(cv2.imdecode(arr, -1), cv2.COLOR_BGR2RGB)
    renderResultOnImage(result, img)
    ig, ax = plt.subplots(figsize=(15, 20))
    ax.imshow(img)
    plt.show()

## Analysis of an image retrieved via URL

# URL direction to image
#urlImage = input('Enter an image URL: ')
urlImage = 'http://s2.thingpic.com/images/rc/bQEtyDiwGtiben3qiCxw7emX.png'

# Computer Vision parameters
params = {'visualFeatures': 'Color,Categories,Description,Tags,Faces'}

headers = dict()
headers['Ocp-Apim-Subscription-Key'] = _key
headers['Content-Type'] = 'application/json'

json_url = {'url': urlImage}
data = None
emotion_headers = dict()
emotion_headers['Ocp-Apim-Subscription-Key'] = _key
emotion_headers['Content-Type'] = 'application/json'
emotion_data = None
emotion_params = None

result = processRequest(json_url, data, headers, params)
emotion_result = processRequest(json_url, emotion_data, emotion_headers, emotion_params)

if result is not None:
    [captions, tags] = getMetadata(result)
    #pprint.pprint(result)
    #displayImage(urlImage)

else:
    captions = "no caption"
    tags = "no result"

print(captions)
print(tags)

type = "motivational"
keyword = "people"
caps = captionsFile.Captions()
refinedCaptions = caps.findCaptionsWith(keyword, type)
print('Refined: ')
print(refinedCaptions)
suggestedCaptions = caps.findRefinedCaptionsWith(tags, refinedCaptions, type)
print('\nFinal suggested: ')
print(suggestedCaptions)


## analyse image stored on disk
'''
# Load raw image file into memory
pathToFileInDisk = r'D:\tmp\3.jpg'
with open(pathToFileInDisk, 'rb') as f:
    data = f.read()

# Computer Vision parameters
params = {'visualFeatures': 'Color,Categories'}

headers = dict()
headers['Ocp-Apim-Subscription-Key'] = _key
headers['Content-Type'] = 'application/octet-stream'

json = None

result = processRequest(json, data, headers, params)

if result is not None:
    # Load the original image, fetched from the URL
    data8uint = np.fromstring(data, np.uint8)  # Convert string to an unsigned int array
    img = cv2.cvtColor(cv2.imdecode(data8uint, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)

    renderResultOnImage(result, img)

    ig, ax = plt.subplots(figsize=(15, 20))
    ax.imshow(img)
'''
