#!/bin/bash

pkill rasa
pkill http-server
pkill java 2>/dev/null
pkill python3
pkill run.sh