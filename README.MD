# eQ Address API

EQ address lookup API provides a simple request service that will return a list of addresses from the Address Index.

You can either build and run a docker container or run in a virtual environment**.  First, clone the repo:

  ```bash
   $ git clone git@github.com:ONSdigital/eq-address-lookup-api.git
   ```
   
## Run a docker container
- Pull from docker hub and run: 
  ```bash
  $ docker run -p 5000:5000 onsdigital/eq-address-lookup-api
  ```
 
## Build and run a Docker container
- Install Docker for your system: https://www.docker.com/
- Build and run the Docker image (make sure you are in the directory of the cloned repo):
  ```bash
   $ docker build ../eq-address-lookup-api
     ...
     Step 11/11 : COPY . /usr/src/app
     ---> 00b93410be43
     Successfully built 00b93410be43
   $ docker run -p 5000:5000 00b93410be43
   ```

## Run in a virtual environment
- Make sure you have a working `pipenv` installation.
- Install dependencies, activate virtual environment and run:
  ```bash
   $ cd eq-address-lookup-api
   $ pipenv install --dev
     ...
   $ pipenv shell
     Spawning environment shell (/bin/bash). Use 'exit' to leave.
     ...
   $ FLASK_APP=application.py flask run
   [2018-04-10 14:05:11.419541] INFO: app: Logging configured
    * Serving Flask app "application"
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)   
  ```

## Usage
To browse the API navigate a browser to `http://localhost:5000`.  You will be redirected to the root of the API at `address_api/`.  :


### Notes
- The `q` parameter is ignored when requesting the root resource.