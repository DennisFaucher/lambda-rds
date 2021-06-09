import mysql.connector
import json
import re

def lambda_handler(event, context):
    conn = mysql.connector.connect(user='admin', password='SuperSecretPassword',
                                  host='hello-mysql.c9kyvjbd9tpz.us-east-1.rds.amazonaws.com',database='dennis')
    
    if conn:
        print ("Connected Successfully")
    else:
        print ("Connection Not Established")
    
    class create_dict(dict): 
      
        # __init__ function 
        def __init__(self): 
            self = dict() 
              
        # Function to add key:value 
        def add(self, key, value): 
            self[key] = value
    
    mydict = create_dict()
    movie_name = event['queryStringParameters']['movie_name']
    clean_movie = re.sub('[^A-Za-z0-9 ]+', '', movie_name)
    select_movie = "select title,popularity,vote_average from dennis.imdb where title like \"" + clean_movie + "%\"  order by popularity desc"
    cursor = conn.cursor()
    cursor.execute(select_movie)
    result = cursor.fetchall()
    
    for row in result:
        mydict.add(row[0],({"popularity":str(row[1]),"vote_average":str(row[2])}))
    
    movie_json = json.dumps(mydict, indent=2)
    
    return movie_json
