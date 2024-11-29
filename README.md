# IM-Assignment2

## How to run the code

Install the dependancies by running the following commands : 

```
python3 -m venv ./rasa-env
source rasa-env/bin/activate
pip install -r requirements.txt
```

Train Rasa :
```
cd rasaDemo
rasa train
cd ..
```

Run the assistant : 
```
./run.sh
```

Stop the assistant : 
```
./stop.sh
```

## Features

- [x] Create / delete repository  
- [x] List user’s organizations  
- [x] List user’s repositories  
- [x] List / Create branch  
- [x] Search in code  
- [x] Show commits history  
- [x] Show repository contributors  
- [x] Subscribe to a repository  
- [x] Repository report
- [x] List repository languages


