# Novisto backend test
> Pre-requisites
Python 3.6.+ or any higher version.

1. 
---
To complete the DB schema, the function "createValueDefinitionTable" was created to execute the following SQL statement:
```
create table IF NOT EXISTS value_definition
(
	id	INTEGER,
	metric_id	INTEGER NOT NULL,
	label	TEXT NOT NULL,
	type	TEXT NOT NULL,
	PRIMARY KEY(id AUTOINCREMENT),
	FOREIGN KEY(metric_id) REFERENCES metric(id)
)
``` 

This function will be executed in the **==function.py==** script. SQL statement "create table IF NOT EXISTS" was created to avoid generating errors every time the script is executed.
  
2.
---
To import the CSV file, follow the next steps:

- Download the attached solution "backend.zip".
- Unzip the file in any location (it is up to you).
- Open the terminal and locate the unzipped folder "backend". **NOTE**: All these files run with python 3.6+ or any higher version (According to the instructions).
- To install all the required libraries, run the following command line in the terminal:
		`pip install -r requirements.txt`
- To import the CSV file, the file **==function.py==** was coded to take the data from the CSV file to the SQLite3 database. The following command line will execute the function. **NOTE**: No matter how many times it runs, the import process will be migrated just once.
		`python function.py`
- The first time the script runs, the messages "CSV loaded!" and "Import script completed!" will appear. If it runs again, just the message "Import script completed!" will be displayed.

3.
---
To complete the API, I have used FastAPI Framework.
**NOTE**: To start the web framework it needs to keep the session in the current terminal. 

- Make sure you are in the `backend` directory: for Windows users, type `cd` otherwise type `pwd`.
- Run the following command line: 
		`python runserver.py`
- In the terminal, the message **"INFO: Application startup complete"** will be displayed. It means that the server is up and running.
- To verify, go to a browser and paste the following address:  (http://127.0.0.1:8000/v1_0/)
- The message **"Welcome to Novisto API V1.0"** will be displayed.

4.
To call the API endpoint, type the following address in a browser: (http://127.0.0.1:8000/v1_0/docs)

One of the advantages of using **FastAPI** is the automatic documentation feature, as it includes Swagger and a list of all the routes including documentation are available.

To see the information read from the database base with the CSV imported data, you can test the `route: /metrics/value-definitions/`

There are routes grouped by **Metrics** and **Value Definitions**. You can test all these routes according to the documentation provided.

**NOTE:** In the API solution, the CSV import has been added just in case you skip running the step two.
