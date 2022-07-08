#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# Name:         Office Status
# Created By:   Matt Shields (GitHub @mattboston)
# Created Date: 2022-07-08
# License:      GPL v3
# =============================================================================

# =============================================================================
# Imports
# =============================================================================
import json
import unicornhat as unicorn
import threading
from time import sleep
import os.path
from pathlib import Path
import logging
import datetime
from random import seed
from random import random

from flask import Flask, jsonify, make_response, request, redirect, url_for, send_from_directory, render_template, send_from_directory
from random import randint

# =============================================================================
# Variables
# =============================================================================
debug = False
state_file = '/opt/officestatus/officestatus.txt'
log_file = '/opt/officestatus/officestatus.log'

# =============================================================================
# App
# =============================================================================
if debug == True:
    debug_level = logging.DEBUG
else:
    debug_level = logging.INFO
logging.basicConfig(filename=log_file, level=debug_level)
logging.info('%s - Started OfficeStatus app' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') )

blinkThread = None
globalRed = 0
globalGreen = 0
globalBlue = 0

#setup the unicorn hat
unicorn.set_layout(unicorn.AUTO)
unicorn.brightness(0.5)
#get the width and height of the hardware
width, height = unicorn.get_shape()

app = Flask(__name__)

seed(1)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

def setColor(r, g, b, brightness, speed) :
    global crntColors, globalBlue, globalGreen, globalRed
    globalRed = r
    globalGreen = g
    globalBlue = b

    if brightness != '' :
        unicorn.brightness(brightness)

    for y in range(height):
        for x in range(width):
            unicorn.set_pixel(x, y, r, g, b)
    unicorn.show()

    if speed != '' :
        sleep(speed)
        unicorn.clear()
        crntT = threading.currentThread()
        while getattr(crntT, "do_run", True) :
             for y in range(height):
                 for x in range(width):
                     unicorn.set_pixel(x, y, r, g, b)
        unicorn.show()
        sleep(speed)
        unicorn.clear()
        unicorn.show()
        sleep(speed)

def switchOff() :
    global blinkThread
    if blinkThread != None :
        blinkThread.do_run = False
    unicorn.clear()
    unicorn.show()
    unicorn.off()

def checkStateFile():
    if not os.path.exists(state_file):
        logging.info("File doesn't exist. Creating new state file.")
        with open(state_file, 'w') as f:
            f.write('free')

def setStatus(status):
    f = open(state_file, "r+")
    f.truncate()
    f.write(status)
    f.close()
    logging.info('Status set to %s' % status)

def getStatus():
    f = open(state_file, "r")
    status = f.readline().splitlines()[0]
    f.close()
    logging.info('Status read %s' % status)
    return status

# API Initialization
@app.route('/')
def root():
    status = getStatus()
    return render_template("index.html", status=status)

@app.route('/off', methods=['POST'])
def off():
    setStatus('free')
    switchOff()
    return redirect("/", code=302)

@app.route('/busy', methods=["POST"])
def busy():
    setStatus('busy')
    switchOff()
    blinkThread = threading.Thread(target=setColor, args=(255, 0, 0, '', ''))
    blinkThread.do_run = True
    blinkThread.start()
    return redirect("/", code=302)

@app.route('/available', methods=['POST'])
def available():
    setStatus('available')
    switchOff()
    blinkThread = threading.Thread(target=setColor, args=(0, 255, 0, '', ''))
    blinkThread.do_run = True
    blinkThread.start()
    return redirect("/", code=302)

@app.route('/away', methods=['POST'])
def away():
    setStatus('away')
    switchOff()
    blinkThread = threading.Thread(target=setColor, args=(0, 0, 255, '', ''))
    blinkThread.do_run = True
    blinkThread.start()
    return redirect("/", code=302)

@app.route('/api/setStatus', methods=['POST'])
def apiSetStatus():
    request_data = request.get_json()
    logging.debug(request_data)
    status = request_data['status']
    setStatus(status)
    switchOff()
    if status == 'busy':
        blinkThread = threading.Thread(target=setColor, args=(255, 0, 0, '', ''))
        blinkThread.do_run = True
        blinkThread.start()
    elif status == 'available':
        blinkThread = threading.Thread(target=setColor, args=(0, 255, 0, '', ''))
        blinkThread.do_run = True
        blinkThread.start()
    elif status == 'away':
        blinkThread = threading.Thread(target=setColor, args=(0, 0, 255, '', ''))
        blinkThread.do_run = True
        blinkThread.start()
    elif status == 'free':
        switchOff()
    return jsonify({ 'status': status })
    
@app.route('/api/status', methods=['GET'])
def apiGetStatus():
    status = getStatus()
    return jsonify({ 'status': status })

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    checkStateFile()
    app.run(host='0.0.0.0', debug=debug, port=80)
