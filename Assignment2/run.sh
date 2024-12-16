#!/bin/bash

# Activate the virtual environment
source rasa-env/bin/activate

# Run rasa
cd rasaDemo
rasa run --enable-api -m ./models/ --cors '*' &
cd ..

# Run FusionEngine
cd FusionEngine
./run.sh &
cd ..

# Run mmiFramework
cd mmiframeworkV2
./run.sh &
cd ..

# Run WebApp
cd WebAppAssistantV2
./run.sh &
cd ..

# Run flask app
python3 app.py &