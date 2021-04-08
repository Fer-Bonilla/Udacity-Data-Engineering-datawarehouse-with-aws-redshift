# -*- coding: utf-8 -*-
"""
    This script implements the ETL pipeline to execute the process using amazon AWS services and redshift DB.
    
    Staging tables:
        - staging_events - Load the raw data from log events json files artist
        auth, firstName, gender, itemInSession,    lastName, length, level, location, method, page, registration, sessionId, song, status, ts, userAgent, userId

        - staging_songs - num_songs artist_id artist_latitude artist_longitude artist_location artist_name song_id title duration year
       
    Dimension tables:
        - users - users in the app: user_id, first_name, last_name, gender, level
        - songs - songs in music database: song_id, title, artist_id, year, duration
        - artists - artists in music database: artist_id, name, location, latitude, longitude
        - time - timestamps of records in songplays: start_time, hour, day, week, month, year, weekday
    
    Fact Table:
        - songplays - records in log data associated with song plays.
        
    The pipeline is implemented using dataframes loading data from Postgres database with the psycopg2 connector.        
        
"""

import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    
    """
        The function load_staging_tables read a json formatted file for songs and events from AWS S3 Bucket 
        into staging raw tables staging_events and staging_songs
        
        Parameters:
            cur (obj): 
                psycopg2 cursor connection object.
            conn (obj): 
                connection object (host, dbname, user, password, port)
    
        Returns:
            None
            
        Note:
            This function writes direct to redshift tables            
    """          
    for query in copy_table_queries:        
        try:
            cur.execute(query)
            conn.commit()
        except psycopg2.Error as e:
            print("Error executing loading staging insert script: "+ query)
            print(e)        
        
        

def insert_tables(cur, conn):
    
    """
        The function insert_tables read the data from raw staging tables to the dimensions and fact tables with format
        and filters applied. 
        
        Parameters:
            cur (obj): 
                psycopg2 cursor connection object.
            conn (obj): 
                connection object (host, dbname, user, password, port)
    
        Returns:
            None
    
        Note:
            This function writes direct to redshift tables
    """     
    for query in insert_table_queries:
        try:
            cur.execute(query)
            conn.commit()
        except psycopg2.Error as e:
            print("Error executing loading dw tables insert script: "+ query)
            print(e)    


def main():
    
    """
        The main function, creates the redshift database connection and initialize the cursor connection and first call
        the load_staging_tables function to read json data to staging tables and then the insert_tables function to 
        write data into the data warehouse tables.
        
        Parameters:
            None
    
        Returns:
            None
    
        Note:
            This function read the configuration parameters from the dwh.cfg file using the psycopg2 library.
    """  
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()