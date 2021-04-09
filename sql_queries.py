import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

# CREATE TABLE staging_events
# LOAD THE DATA FROM SONGS JSON FILES

staging_events_table_create= ("""
    CREATE TABLE staging_events (
          artist            VARCHAR,
          auth              VARCHAR,
          firstName         VARCHAR,
          gender            VARCHAR,
          itemInSession     VARCHAR,
          lastName          VARCHAR,
          length            VARCHAR,
          level             VARCHAR,
          location          VARCHAR,
          method            VARCHAR,
          page              VARCHAR,
          registration      VARCHAR,
          sessionId         INTEGER,
          song              VARCHAR,
          status            VARCHAR,
          ts                BIGINT,
          userAgent         VARCHAR,
          userId            INTEGER
          );                           
""")

# CREATE TABLE staging_events
# LOAD THE DATA FROM SONGS JSON FILES

staging_songs_table_create = ("""
    CREATE TABLE staging_songs (
          num_songs         INTEGER,
          artist_id         VARCHAR,
          artist_latitude   DECIMAL,
          artist_longitude  DECIMAL,
          artist_location   VARCHAR,
          artist_name       VARCHAR,
          song_id           VARCHAR,
          title             VARCHAR,
          duration          DECIMAL,
          year              INTEGER
          );
""")

# CREATE TABLE songplay (FACTABLE)
# LOAD THE DATA FROM STAGING TABLES

songplay_table_create = ("""
    CREATE TABLE songplay (
          songplay_id       INTEGER IDENTITY(0,1)   NOT NULL SORTKEY,
          start_time        TIMESTAMP               NOT NULL,
          user_id           INTEGER                 NOT NULL,
          level             VARCHAR(20)             NULL,
          song_id           VARCHAR(20)             NOT NULL,
          artist_id         VARCHAR(20)             NOT NULL,
          session_id        INTEGER                 NOT NULL,
          location          VARCHAR                 NULL,
          user_agent        VARCHAR                 NULL
      );
""")

# CREATE TABLE user (DIMENSION)
# LOAD THE DATA FROM STAGING TABLES

user_table_create = ("""
    CREATE TABLE users (
          user_id       INTEGER         NOT NULL    SORTKEY,
          first_name    VARCHAR(255)    NULL,
          last_name     VARCHAR(255)    NULL,
          gender        VARCHAR(1)      NULL,
          level         VARCHAR(20)     NULL
      );  
""")

# CREATE TABLE song (DIMENSION)
# LOAD THE DATA FROM SONGS JSON FILES

song_table_create = ("""
    CREATE TABLE songs (
          song_id        VARCHAR(20)     NULL,
          title          VARCHAR(255)    NULL,
          artist_id      VARCHAR(20)     NULL,
          duration       DECIMAL         NULL,
          year           INTEGER         NULL
        ) DISTSTYLE ALL;  
""")

# CREATE TABLE artist (DIMENSION)
# LOAD THE DATA FROM STAGING TABLES

artist_table_create = ("""
    CREATE TABLE artists (
          artist_id       VARCHAR(20)     NULL,
          name            varchar(255)    NULL,
          location        VARCHAR(255)    NULL,
          latitude        DECIMAL         NULL,
          longitude       DECIMAL         NULL
        ) DISTSTYLE ALL;  
""")

# CREATE TABLE time (DIMENSION)
# LOAD THE DATA FROM STAGING TABLES

time_table_create = ("""
    CREATE TABLE time (
          start_time      TIMESTAMP       NOT NULL     SORTKEY,
          hour            INTEGER         NULL,
          day             INTEGER         NULL,
          week            INTEGER         NULL,
          month           INTEGER         NULL,
          year            INTEGER         NULL,
          weekday         INTEGER         NULL
        ) DISTSTYLE ALL;  
""")



# STAGING TABLES

staging_events_copy = ("""
copy staging_events from {}
credentials 'aws_iam_role={}' 
format as json {};
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""
copy staging_songs from {}
credentials 'aws_iam_role={}' 
json 'auto';
""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])


# FINAL TABLES
# INSERT SQL SCRIPT

# INSERT DATA INTO FACTABLE songplay  
songplay_table_insert = ("""
    INSERT INTO songplay (              start_time,
                                        user_id,
                                        level,
                                        song_id,
                                        artist_id,
                                        session_id,
                                        location,
                                        user_agent)
    SELECT  TIMESTAMP 'epoch' + e.ts/1000 * interval '1 second' as start_time,                
            e.userId                   AS user_id,
            e.level                    AS level,
            s.song_id                  AS song_id,
            s.artist_id                AS artist_id,
            e.sessionId                AS session_id,
            e.location                 AS location,
            e.userAgent                AS user_agent
    FROM staging_events AS e
    JOIN staging_songs AS s
    ON (e.artist = s.artist_name)
    WHERE e.page = 'NextSong';
""")


# INSERT DATA INTO FACTABLE songplay
user_table_insert = ("""
    INSERT INTO users (                user_id,
                                       first_name,
                                       last_name,
                                       gender,
                                       level)
    SELECT  DISTINCT e.userId          AS user_id,
            e.firstName                AS first_name,
            e.lastName                 AS last_name,
            e.gender                   AS gender,
            e.level                    AS level
    FROM staging_events AS e
    WHERE e.page = 'NextSong';
""")


# INSERT DATA INTO FACTABLE songplay
song_table_insert = ("""
    INSERT INTO songs (                 song_id,
                                        title,
                                        artist_id,
                                        year,
                                        duration)
    SELECT  DISTINCT s.song_id          AS song_id,
            s.title                     AS title,
            s.artist_id                 AS artist_id,
            s.year                      AS year,
            s.duration                  AS duration
    FROM staging_songs AS s;
""")


# INSERT DATA INTO FACTABLE songplay
artist_table_insert = ("""
    INSERT INTO artists (               artist_id,
                                        name,
                                        location,
                                        latitude,
                                        longitude)
    SELECT  DISTINCT s.artist_id        AS artist_id,
            s.artist_name               AS name,
            s.artist_location           AS location,
            s.artist_latitude           AS latitude,
            s.artist_longitude          AS longitude
    FROM staging_songs AS s;
""")


# INSERT DATA INTO FACTABLE songplay
time_table_insert = ("""
    INSERT INTO time (start_time,
                      hour,
                      day,
                      week,
                      month,
                      year,
                      weekday)          
    SELECT  TIMESTAMP 'epoch' + e.ts/1000 * interval '1 second' as start_time,   
            EXTRACT(hour FROM start_time)    AS hour,
            EXTRACT(day FROM start_time)     AS day,
            EXTRACT(week FROM start_time)    AS week,
            EXTRACT(month FROM start_time)   AS month,
            EXTRACT(year FROM start_time)    AS year,
            EXTRACT(week FROM start_time)    AS weekday
    FROM    staging_events                   AS e
    WHERE   e.page = 'NextSong';
""")


# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [artist_table_drop, song_table_drop, time_table_drop, user_table_drop, songplay_table_drop, staging_songs_table_drop, staging_events_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [user_table_insert, song_table_insert, artist_table_insert, time_table_insert, songplay_table_insert]