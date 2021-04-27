# Project: Data Warehouse

## Project Overview:

<ul>A music streaming platform, <strong>Sparkify</strong> has grown their user and song database and want to move their data onto the cloud.So the data resides in s3 in a directory of JSON logs and JSON metadata.As a DataEngineer we are going to build a ETL pipeline in this project to extract that data from s3, stages them in Redshift.</ul><br>

## Project Files:
The files in this repository are :
- Project Datasets
- sql_queries.py
- create_tables.py
- dwh.cfg
- etl.py
- README.md
<br>

**Project Datasets/** - We have two datasets that reside in S3. Here are the S3 links for each:

- Song data: s3://udacity-dend/song_data
- Log data: s3://udacity-dend/log_data
- Log data json path: s3://udacity-dend/log_json_path.json
.
- 1. 'log_data/' - It contains JSON files related to songplay log data.

ex:
    {"artist":null,
     "auth":"Logged In",  
     "firstName":"Walter",  
     "gender":"M",  
     "itemInSession":0,
     "lastName":"Frye",
     "length":null,
     "level":"free",  
     "location":"San Francisco-Oakland-Hayward, CA",  
     "method":"GET",  
     "page":"Home",
     "registration":1540919166796.0,  
     "sessionId":38,  
     "song":null,
     "status":200,  
     "ts":1541105830796,  <br>
     "userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"",  <br>
     "userId":"39"
     }
- 2. 'song_data/' - It has JSON files that contains metadata about song and artist of that song.

ex:
    {"num_songs": 1,<br>
     "artist_id": "ARJIE2Y1187B994AB7",<br>
     "artist_latitude": null, <br>
     "artist_longitude": null,<br>
      "artist_location": "",<br>
      "artist_name": "Line Renaud",<br>
      "song_id": "SOUPIRU12A6D4FA1E1", <br>
      "title": "Der Kleine Dompfaff",<br>
      "duration": 152.92036, <br>
      "year": 0}

**sql_queries.py** - <ul>This script file contains all the SQL commands used to create , drop and insert  values into the two other files.</ul>

**dwh.cfg** -<ul>This files contains all the information required to setup the cluster on AWS and also details related to S3, IAM role and connection details.</ul>

**create_tables.py** - <ul>In this script file, we will create the fact and dimension tables for the star schema in Redshift.</ul>

**etl.py** -<ul> In this script file, we will load data from S3 into staging tables on Redshift and then process that data into the analytics tables on Redshift.</ul>

**README.md** - <ul>It provides details information about the project.</ul>

<br>

## Sparkify DataSchema :
The DataSchema has 7 tables represented in a Star schema.

#### Staging Tables -
- staging_events-It is the stating table for event data.
- staging_songs-It is the staging table for song data.

#### Fact Table -
- songplays - It has records in log data associated with song plays.  

#### Dimension Tables -
- users - It has data about the users in the app.
- songs - It has data about the songs in music database.
- artists - It has data about the artists in music database.
- time - It has data about the timestamps of records in songplays broken down into specific units.

## Project Steps :
#### Step1 :-
<ul>Here we need to design schemas for the fact and dimension tables.We need to write create ,drop and insert statements for each table in <em>'sql_queries.py'</em> file.</ul>

#### Step2 :-
<ul>Launch the redshift cluster.And add the redshift database and IAM role information to the <em>'dwh.cfg'</em> file </ul>

#### Step3 :-
<ul>Run the <em>'create_tables.py'</em> to create all tables in Redshift.You can run <em>'create_tables.py'</em> file.We can test the files using the Redshift query editor.</ul>
- !python create_tables.py

#### Step4 :-
<ul>Run the <em>'etl.py'</em> to load data from S3 to staging tables on Redshift and also to load data from staging tables to analytics table on Redshift.We can query the data from the tables using the Query editor and check whether the data is loaded correctly or not.</ul>
- !python etl.py

#### Step5 :-
<ul> Delete the redshift cluster when finished. </ul>
