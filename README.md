# GreenFlow

## Description

A brief overview of what the project does and its purpose.

## Features

* Rest API Endpoints (base URL: http://localhost:8080/):
  * Summary (returns a breave list of information pertaning the DataSet)
  * cleanDataSet (Cleans The DataSet of missing data from rows and extra spaces)
  * parquettodb (Inserts the DataSet after the Clean up process into MongoDB with the collection name being the name of the file [filename]
* 

## Installation

1. Clone the repository:

   ```
   git clone git@github.com:HCorte/GreenFlow.git
   ```
2. Navigate to the project directory:

   ```
   cd your-repo
   ```
3. Install Virtual Environment

   ```
   python -m venv venv
   ```
4. Activate Virtual Environment

   ```
   source venv/bin/active
   ```
5. Install dependencies (inside the Virtual Environment):

```
   pip install -r requirements.txt
```


## Usage

* Run the project:

  ```
  python src/api.py
  ```
* Open in browser at `<span>http://localhost:8080/Summary</span>` to make a simple test
* Import from the folder postman the collection to postman by:

  * Open Postman -> Select File -> Select "Import..." -> then select the collection inside the postman folder of this project.

## To create Dockers Containers

* Build and run containers
  ```
  docker compose up --build
  ```
* Now can call as usuall the endpoints from postman and the app in container will respond and save in a second container the db as well backup in the host in this project data folder.

## Contributing

* Rest API
* Create a new branch
* Make your changes and commit

## License

This project is licensed under the MIT License.
