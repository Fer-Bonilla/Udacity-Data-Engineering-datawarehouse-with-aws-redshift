import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplay;"
user_table_drop = "DROP TABLE IF EXISTS user;"
song_table_drop = "DROP TABLE IF EXISTS song;"
artist_table_drop = "DROP TABLE IF EXISTS artist;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

# CREATE TABLE staging_events
# LOAD THE DATA FROM SONGS JSON FILES

staging_events_table_create= ("""
    CREATE TABLE staging_events (
      artist            VARCHAR         NULL,
      auth              VARCHAR         NULL,
      firstName         VARCHAR         NULL,
      gender            VARCHAR         NULL,
      itemInSession     VARCHAR         NULL,
      lastName          VARCHAR         NULL,
      length            VARCHAR         NULL,
      level             VARCHAR         NULL,
      location          VARCHAR         NULL,
      method            VARCHAR         NULL,
      page              VARCHAR         NULL,
      registration      VARCHAR         NULL,
      sessionId         INTEGER         NULL,
      song              VARCHAR         NULL,
      status            VARCHAR         NULL,
      ts                TIMESTAMP       NULL,
      userAgent         VARCHAR         NULL,
      userId            INTEGER         NULL,
      );                           
""")

# CREATE TABLE staging_events
# LOAD THE DATA FROM SONGS JSON FILES

staging_songs_table_create = ("""
    CREATE TABLE staging_events (
      num_songs         INTEGER         NULL,
      artist_id         VARCHAR         NULL,
      artist_latitude   VARCHAR         NULL,
      artist_longitude  VARCHAR         NULL,
      artist_location   VARCHAR         NULL,
      artist_name       VARCHAR         NULL,
      song_id           VARCHAR         NULL,  
      title             VARCHAR         NULL,
      duration          DECIMAL         NULL,
      year              INTEGER         NULL
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
    CREATE TABLE staging_events (
      user_id           INTEGER         NOT NULL    sortkey distkey,
      first_name        VARCHAR(255)    NULL,
      last_name         VARCHAR(255)    NULL,
      gender            VARCHAR(1)      NULL,
      level             VARCHAR(20)    NULL
      );  
""")

# CREATE TABLE song (DIMENSION)
# LOAD THE DATA FROM SONGS JSON FILES

song_table_create = ("""
    CREATE TABLE song (
      song_id        VARCHAR(20)     NOT NULL    sortkey distkey,
      title          VARCHAR(255)    NULL,
      artist_id      VARCHAR(20)     NULL,
      duration       DECIMAL         NULL,
      year           INTEGER         NULL
    ) DISTYLE ALL;  
""")

# CREATE TABLE artist (DIMENSION)
# LOAD THE DATA FROM STAGING TABLES

artist_table_create = ("""
    CREATE TABLE artist (
      artist_id       VARCHAR(20)         NOT NULL    sortkey distkey,
      name            varchar(255)    NULL,
      location        VARCHAR(255)     NULL,
      lattitude       INTEGER         NULL,
      longitude       INTEGER         NULL,
    ) DISTYLE ALL;  
""")

# CREATE TABLE time (DIMENSION)
# LOAD THE DATA FROM STAGING TABLES

time_table_create = ("""
    CREATE TABLE time (
      start_time     TIMESTAMP       NOT NULL SORTKEY,
      hour           INTEGER         NULL,
      day            INTEGER         NULL,
      week           INTEGER         NULL,
      month          INTEGER         NULL,
      year           INTEGER         NULL,
      weekday        INTEGER         NULL
    ) DISTYLE ALL;  
""")



# STAGING TABLES

staging_events_copy = ("""
    COPY staging_events FROM {}
    credentials 'aws_iam_role={}'
    format as json {}
    STATUPDATE ON
    region 'us-west-2';
""").format(LOG_DATA, ARN, LOG_JSONPATH)

staging_songs_copy = ("""
    COPY staging_songs FROM {}
    credentials 'aws_iam_role={}'
    format as json 'auto'
    ACCEPTINVCHARS AS '^'
    STATUPDATE ON
    region 'us-west-2';
""").format(SONG_DATA, ARN)

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays (             start_time,
                                        user_id,
                                        level,
                                        song_id,
                                        artist_id,
                                        session_id,
                                        location,
                                        user_agent)
    SELECT  DISTINCT TIMESTAMP 'epoch' + se.ts/1000 \
                * INTERVAL '1 second'   AS start_time,
            se.userId                   AS user_id,
            se.level                    AS level,
            ss.song_id                  AS song_id,
            ss.artist_id                AS artist_id,
            se.sessionId                AS session_id,
            se.location                 AS location,
            se.userAgent                AS user_agent
    FROM staging_events AS se
    JOIN staging_songs AS ss
        ON (se.artist = ss.artist_name)
    WHERE se.page = 'NextSong';
""")

user_table_insert = ("""
    INSERT INTO users (                 user_id,
                                        first_name,
                                        last_name,
                                        gender,
                                        level)
    SELECT  DISTINCT se.userId          AS user_id,
            se.firstName                AS first_name,
            se.lastName                 AS last_name,
            se.gender                   AS gender,
            se.level                    AS level
    FROM staging_events AS se
    WHERE se.page = 'NextSong';
""")

song_table_insert = ("""
    INSERT INTO songs (                 song_id,
                                        title,
                                        artist_id,
                                        year,
                                        duration)
    SELECT  DISTINCT ss.song_id         AS song_id,
            ss.title                    AS title,
            ss.artist_id                AS artist_id,
            ss.year                     AS year,
            ss.duration                 AS duration
    FROM staging_songs AS ss;
""")

artist_table_insert = ("""
    INSERT INTO artists (               artist_id,
                                        name,
                                        location,
                                        latitude,
                                        longitude)
    SELECT  DISTINCT ss.artist_id       AS artist_id,
            ss.artist_name              AS name,
            ss.artist_location          AS location,
            ss.artist_latitude          AS latitude,
            ss.artist_longitude         AS longitude
    FROM staging_songs AS ss;
""")

time_table_insert = ("""
    INSERT INTO time (start_time,
                      hour,
                      day,
                      week,
                      month,
                      year,
                      weekday)
    SELECT  DISTINCT TIMESTAMP 'epoch' + se.ts/1000 \
                * INTERVAL '1 second'        AS start_time,
            EXTRACT(hour FROM start_time)    AS hour,
            EXTRACT(day FROM start_time)     AS day,
            EXTRACT(week FROM start_time)    AS week,
            EXTRACT(month FROM start_time)   AS month,
            EXTRACT(year FROM start_time)    AS year,
            EXTRACT(week FROM start_time)    AS weekday
    FROM    staging_events                   AS se
    WHERE se.page = 'NextSong';
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
