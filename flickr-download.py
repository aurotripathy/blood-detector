#! /usr/bin/env python
# downloads images from flickr with a certain tag

# PREREQUISITE pip-install flickrapi

# These are the size of images that you want
# url_c: URL of medium 800, 800 on longest size image
# url_m: URL of small, medium size image
# url_n: URL of small, 320 on longest side size image
# url_o: URL of original size image
# url_q: URL of large square 150x150 size image
# url_s: URL of small suqare 75x75 size image
# url_sq: URL of square size image
# url_t: URL of thumbnail, 100 on longest side size image

import os
from shutil import rmtree
from flickrapi import FlickrAPI
from PIL import Image
import requests
from StringIO import StringIO

#from pudb import set_trace
#set_trace()

images_dir = 'images'
if os.path.isdir(images_dir): # start clean
    rmtree(images_dir)
os.makedirs(images_dir)

# You'll need your own API credentials
API_KEY =  '91db0c8b9557b92f5b5f8db0b96a9f9f'
API_SECRET = 'fd983d4ea5b198d9'
per_page = 100
flickr = FlickrAPI(API_KEY, API_SECRET)
extras='url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'

# this should yield 64 images
for photo in flickr.walk(tags='blood',
                         license=8, # just the government works
                         sort='relevance',
                         per_page=per_page,
                         extras=extras):
    url = photo.get('url_c')
    if url != None:
        response = requests.get(url)
        img = Image.open(StringIO(response.content))
        img.save(images_dir + '/' + os.path.basename(url))

# references:
# http://joequery.me/code/flickr-api-image-search-python/
# https://stuvel.eu/flickrapi-doc/

# to understand the licenses
# https://www.flickr.com/services/api/flickr.photos.licenses.getInfo.html







