# SMS-Queue-System

## Setup and Installation
Before begin, ensure you have the following
1. Python
2. Redis
3. MySQL

### Setup Python
Update the package list and install python
```sh
sudo apt update
sudo apt install python3 python3-venv python3-pip
```
put the required libraries(pandas, mysql-connector-python, flask, redis, rq, requests) in requirement.txt file
```sh
pip install -r requirements.txt
```

### Setup Redis
Linux
```sh
sudo apt update
sudo apt install redis-server
```
Start the Redis-server
```sh
sudo systemctl start redis
```
Check the status of Redis-server
```sh
systemctl status redis-server
```
### Setup MySQL
- Start the MySQL server.
- Create a database and user with appropriate privileges.
- Update your configuration file with the MySQL credentials.

## Running the Project
### Starting the flask application
```sh
python3 App.py  # Main Flask application
```
### Running the RQ worker
```sh
python3 worker.py  # RQ worker script
```
### Running the Mass SMS Script
```sh
python3 mass_sms.py  # Script to enqueue SMS jobs
```

Details functionalities of the code is written inside the .py files in comments.






