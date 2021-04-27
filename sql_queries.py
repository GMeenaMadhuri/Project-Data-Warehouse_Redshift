import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

IAM_ROLE = config['IAM_ROLE']['ARN']
LOG_DATA = config['S3']['LOG_DATA']
LOG_JSONPATH = config['S3']['LOG_JSONPATH']
SONG_DATA = config['S3']['SONG_DATA']

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events(
                                      artist VARCHAR ,
                                      auth VARCHAR ,
                                      firstName VARCHAR(50),
                                      gender CHAR ,
                                      itemInSession INTEGER,
                                      lastName VARCHAR(50),
                                      length FLOAT ,
                                      level VARCHAR ,
                                      location VARCHAR,
                                      method VARCHAR ,
                                      page VARCHAR ,
                                      registration FLOAT ,
                                      sessionId INTEGER  SORTKEY DISTKEY,
                                      song VARCHAR ,
                                      status INTEGER ,
                                      ts BIGINT ,
                                      userAgent VARCHAR ,
                                      userId INTEGER );
""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs(
                                        num_songs INTEGER ,
                                        artist_id VARCHAR  SORTKEY DISTKEY,
                                        artist_latitude FLOAT ,
                                        artist_longitude FLOAT ,
                                        artist_location VARCHAR ,
                                        artist_name VARCHAR ,
                                        song_id VARCHAR  ,
                                        title VARCHAR ,
                                        duration FLOAT ,
                                        year FLOAT );
""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays(
                                songplay_id INTEGER IDENTITY(0,1) NOT NULL SORTKEY,
                                start_time timestamp NOT NULL,
                                user_id int NOT NULL DISTKEY,
                                level varchar NOT NULL,
                                song_id varchar,
                                artist_id varchar,
                                session_id int NOT NULL,
                                location varchar NOT NULL,
                                user_agent varchar NOT NULL);
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users(
                            user_id int PRIMARY KEY SORTKEY,
                            first_name varchar NOT NULL,
                            last_name varchar NOT NULL,
                            gender varchar NOT NULL,
                            level varchar NOT NULL)diststyle all;

""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs(
                            song_id varchar PRIMARY KEY SORTKEY,
                            title varchar NOT NULL,
                            artist_id varchar NOT NULL,
                            year int NOT NULL,
                            duration numeric NOT NULL);
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists(
                                artist_id varchar PRIMARY KEY SORTKEY,
                                name varchar NOT NULL,
                                location varchar ,
                                latitude numeric ,
                                longitude numeric)diststyle all;
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time(
                            start_time timestamp PRIMARY KEY SORTKEY,
                            hour int NOT NULL,
                            day int NOT NULL,
                            week int NOT NULL,
                            month int NOT NULL,
                            year int NOT NULL,
                            weekday varchar NOT NULL)diststyle all;
""")

# STAGING TABLES

staging_events_copy = ("""COPY staging_events FROM {}
credentials 'aws_iam_role={}'
region 'us-west-2'
format as json {};
""").format(LOG_DATA,IAM_ROLE,LOG_JSONPATH)

staging_songs_copy = ("""COPY staging_songs FROM {}
credentials 'aws_iam_role={}'
region 'us-west-2'
json 'auto'
""").format(SONG_DATA, IAM_ROLE)

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplays(
                        start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
                        SELECT TIMESTAMP 'epoch' + se.ts/1000 * interval '1 second' as start_time,
                                    se.userid,
                                    se.level,
                                    ss.song_id,
                                    ss.artist_id,
                                    se.sessionid,
                                    se.location,
                                    se.useragent
                        FROM staging_events se
                        JOIN staging_songs ss ON ( se.song = ss.title and se.artist = ss.artist_name)
                        WHERE se.page = 'NextSong';
""")

user_table_insert = ("""INSERT INTO users
                        SELECT DISTINCT userId, firstName, lastName, gender, level
                        from staging_events
                        WHERE userId IS NOT NULL
                        AND page = 'NextSong';

""")

song_table_insert = ("""INSERT INTO songs
                        SELECT DISTINCT song_id,
                                        title ,artist_id ,year ,duration
                        from staging_songs
                        where song_id IS NOT NULL;
""")

artist_table_insert = ("""INSERT INTO artists
                        SELECT DISTINCT artist_id,
                                artist_name, artist_location, artist_latitude, artist_longitude
                        FROM staging_songs;
""")

time_table_insert = ("""INSERT INTO  time
       SELECT DISTINCT TIMESTAMP 'epoch' + (ts/1000) * INTERVAL '1 second' as start_time,
               EXTRACT(HOUR FROM start_time) AS hour,
               EXTRACT(DAY FROM start_time) AS day,
               EXTRACT(WEEKS FROM start_time) AS week,
               EXTRACT(MONTH FROM start_time) AS month,
               EXTRACT(YEAR FROM start_time) AS year,
               to_char(start_time, 'Day') AS weekday
       FROM staging_events;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
