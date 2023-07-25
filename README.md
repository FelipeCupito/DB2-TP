# Pixie - FastAPI Web API Application with Docker
Pixie is a project that utilizes FastAPI and Docker to create and run a web API application. The following instructions will guide you through setting up and running the project in your local environment.

## Prerequisites
Before proceeding, make sure you have the following programs installed on your machine:
- Docker: [Installation Guide](https://docs.docker.com/get-docker/)
- Python 3.8: [Installation Guide](https://www.python.org/downloads/)
## Setup Instructions
Grant execution permissions to the setup scripts:
```bash
cd BD2-TP
chmod +x setup.sh
```

## Running the application
1. Run the `setup.sh` script to add permissions to run the script, build the Docker image, and run the container:
```bash
sudo ./setup.sh
```
2. Start the bank1 application by running the `run_bank1.sh` script:
```bash
 ./run_bank1.sh
```
this will start the bank1 application on port 8080

3. Start the bank2 application by running the `run_bank2.sh` script:
```bash
 ./run_bank2.sh
```
this will start the bank2 application on port 8090

4. Start the pixie application by running the `run_pixie.sh` script:
```bash
 ./run_pixie.sh
```
this will start the pixie application on port 8000

4. Start the frontend application by running the following commands:
```python
 pip install streamlit
 pip install requests
 cd frontend
 streamlit run home.py --server.enableCORS false --server.enableXsrfProtection false
```
this will start the frontend application on port 8501

## Stopping the application
If you wish to stop the application execution, simply press `Ctrl + C` in the terminal where the application is running. This will stop the FastAPI development server.

## Additional Notes
To change the port of the applications, navigate to the corresponding `run_bank1.sh`, `run_bank2.sh`, or `run_pixie.sh` file. Inside the file, you'll find a line similar to `python3 main.py 8080 5432 "data/user1.json"`. Change the value of the first parameter passed to main.py to modify the port. For example, if you want bank 1 to run on port 8081, modify the file to `python3 main.py 8081 5432 "data/user1.json"`.

## Authors
- 60058 - Felipe Cupitó
- 60072 - Malena Vasquez Currie
- 61278 - Sol Victoria Anselmo
