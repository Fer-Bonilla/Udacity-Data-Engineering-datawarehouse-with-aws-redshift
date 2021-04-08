# -*- coding: utf-8 -*-
"""
    This script implements the DDL scripts for creating the schema in the redshift database. First, try to drop all
    the tables if they exist and create the structure of the table. This is part of the data pipeline program.        
"""

import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
        The function drop_tables executes the drop tables scripts described in the sql_queries.py
        
        Parameters:
            cur (obj): 
                psycopg2 cursor connection object.
            conn (obj): 
                connection object (host, dbname, user, password, port)
    
        Returns:
            None
                      
    """       
    for query in drop_table_queries:
        try:
            cur.execute(query)
            conn.commit()
        except psycopg2.Error as e:
            print("Error executing drop tale script: "+ query)
            print(e)
                  

def create_tables(cur, conn):
    """
        The function create_tables executes the create tables scripts described in the sql_queries.py
        
        Parameters:
            cur (obj): 
                psycopg2 cursor connection object.
            conn (obj): 
                connection object (host, dbname, user, password, port)
    
        Returns:
            None         
    """       
    for query in create_table_queries:
        try:
            cur.execute(query)
            conn.commit()
        except psycopg2.Error as e:
            print("Error creating table: "+ query)
            print(e)        

        

def main():
    
    """
        The main function, creates the redshift database connection and initialize the cursor connection and first call
        the drop_tables function to execute drop tables script and then the create_tables executes the create tables sql
        scripts to create the stating and the datawarehouse redshift tables.
        
        Parameters:
            None
    
        Returns:
            None
    
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
       
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))      
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()