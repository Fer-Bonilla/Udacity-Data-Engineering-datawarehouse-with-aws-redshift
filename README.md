# Data Warehouse with AWS Redshift

This repository is for the third Data Engineering Nanodegree project from Udacity. This project implements a Data warehouse model with and Amazon Redshift:

- Understanding the problem to solve
- Modeling the database and pipeline model
- Create the database schema
- ETL development in Python


## Problem understanding

Define fact and dimension tables for a star schema for a particular analytic focus and write an ETL pipeline that transfers data from files in two local directories into these tables in Postgres using Python and SQL. The task is to create a database schema and upload the data into a PostgreSQL database and implement an ETL pipeline for this analysis.


## Data description

The project uses data from [Million Song Dataset](https://labrosa.ee.columbia.edu/millionsong/) that is a freely-available collection of audio features and metadata for a million contemporary popular music tracks (300 GB). This data is open for exploration and research and for this project will only use a sample from the songs database and artist information in json format.
  
- **Song dataset**:  
  Json files are under */data/song_data* directory. The file format is:

```
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

- **Log dataset**: 
  Json File are under */data/log_data*. The file format is:

```
{"artist":"Slipknot","auth":"Logged In","firstName":"Aiden","gender":"M","itemInSession":0,"lastName":"Ramirez","length":192.57424,"level":"paid","location":"New York-Newark-Jersey City, NY-NJ-PA","method":"PUT","page":"NextSong","registration":1540283578796.0,"sessionId":19,"song":"Opium Of The People (Album Version)","status":200,"ts":1541639510796,"userAgent":"\"Mozilla\/5.0 (Windows NT 6.1) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"","userId":"20"}
```
## Database Model

The database will be designed for analytics using Fact and Dimensions tables on a Star Schema architecture, and staging tables to read data from s3 data storage:

**Staging Tables**

  staging_events - Load the raw data from log events json files
  artist, auth, firstName, gender, itemInSession, lastName, length, level, location, method, page, registration, sessionId, song, status, ts, userAgent, userId

  staging_songs
  num_songs	artist_id	artist_latitude	artist_longitude	artist_location	artist_name	song_id	title	duration	year
  

**Fact Table**

  songplays - records in log data associated with song plays i.e. records with page NextSong
    songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent


**Dimension Tables**

  users - users in the app: user_id, first_name, last_name, gender, level
  songs - songs in music database: song_id, title, artist_id, year, duration
  artists - artists in music database: artist_id, name, location, latitude, longitude
  time - timestamps of records in songplays broken down into specific units: start_time, hour, day, week, month, year, weekday


### Logic model

![Logic model](https://github.com/Fer-Bonilla/Udacity-Data-Engineering-data-modeling-with-postgres/blob/main/images/ERD_Postgres_Database.png)


## Project structure

The project structure is based on the Udacity's project template:
1. **test.ipynb** displays the first few rows of each table to let you check your database
2. **create_tables.py** drops and creates your tables. You run this file to reset your tables before each time you run your ETL scripts
3. **etl.ipynb** reads and processes a single file from song_data and log_data and loads the data into your tables
5. **etl.py** reads and processes files from song_data and log_data and loads them into the databse tables
7. **sql_queries.py** contains all the sql queries for create and fill the tables
8. **README.md** provides discussion on your project

## ETL Pipeline description

### etl.py
The ETL process is developed in the etl.py script. Data is load from the JSON files first from the songs dataset and extracting song_id, title, artist_id, year, duration columns and filling the songs table and artist table. (function process_song_file). The second dataset is load from logs files to fill the tables time and users. In both cases, the data is loaded to pandas data frames, and then cleaned and filtered and using psycopg2 the SQL insert scripts (sql_queries) to fill all the tables.

### ETL pipeline diagram

![ETL pipeline diagram](https://github.com/Fer-Bonilla/Udacity-Data-Engineering-data-modeling-with-postgres/blob/main/images/ETL_Pipeline.png)

## Instructions to run the pipeline

A. Componentes required
  1. Postgres dabase 
  2. Jupyter notebooks environment available
  3. Python packages: psycopg2, pandas and python-sql

B Running the pipeline

  1. Clone the respository
  2. Run create_tables.py (Drop tables and create again)
  4. Run etl.py (Run the ETL process)
  5. Run test.ipynb notebook to validate with son example querys

## Author 
Fernando Bonilla [linkedin](https://www.linkedin.com/in/fer-bonilla/)
