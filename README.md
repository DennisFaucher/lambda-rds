ret![Lambda Select](https://user-images.githubusercontent.com/9034190/120943381-82982780-c6fc-11eb-8506-bf97290f80c8.png)
# AWS Lambda Serverless RDS MySQL Tutorial
![Lambda](https://user-images.githubusercontent.com/9034190/120906888-25807100-c62b-11eb-94fa-686113054719.png)

## Credits

I would like to thank the people whose blogs I read as well as two specific AWS Heroes - [Ben Kehoe](https://twitter.com/ben11kehoe) and [Chris Williams](https://twitter.com/mistwire) for assistance.

## Why

![Question Mark](https://user-images.githubusercontent.com/9034190/120907020-0b935e00-c62c-11eb-8460-4bf18c265704.png)

I don't actually remember. :smiley: I have been working my way through an AWS certification and it was probably the section on RDS serverless databases that gave me the idea "What if I could create a free database search app using Lambda and RDS?" Lambda functions are free up to a point and there is a free RDS database tier. So off I went...

## How

![Tools](https://user-images.githubusercontent.com/9034190/120907232-dbe55580-c62d-11eb-9a65-27f4d2707c71.png)

### Parts List

* An AWS Account. You can create one [here](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html)
* The mysql-client installed on your computer. On my Mac, I installed with:

````bash
brew install mysql-client
````

On Linux, you should be able to install the mysql-client package with your favorite package manager.

### Create the Serverless RDS Database

#### Create the Database Instance

OK, let's create a free serverless database. Login to your AWS Management [Console](https://aws.amazon.com/console/) and choose All Services and then Database > RDS.

![RDS](https://user-images.githubusercontent.com/9034190/120907486-e43e9000-c62f-11eb-9c8f-02e02deb8c63.png)

* Choose the Create Database button 

![Create Database](https://user-images.githubusercontent.com/9034190/120907637-25836f80-c631-11eb-9669-7c7abb358bc7.png)

* Select Easy Create, MySql, Free Tier

![Create DB 1](https://user-images.githubusercontent.com/9034190/120907732-e6095300-c631-11eb-855e-ff8aa75741a8.png)

* Give your database instance a name, create an admin password and select the Create database button

![Create DB 2](https://user-images.githubusercontent.com/9034190/120907754-1d77ff80-c632-11eb-9506-d19b09996696.png)

You will be redirected to the Databases screen and will see that your database is being created. This will take a few minutes

![DB Creating](https://user-images.githubusercontent.com/9034190/120907803-a131ec00-c632-11eb-97cb-e9c6d1271d2e.png)

Make sure you can access your new database server

* Use a Security Group that has port 3306 open for your database instance. AWS Security Groups are a _huge_ topic that I will not explain here. Please see [this page](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) for a tutorial on AWS Security Groups.
* Give the database instance a public IP address. This is not recommended, but made accessing the database instance from non-AWS machines (my laptop) much easier. To give the database instance a public IP address, select the radio button for your database in the database list, select the Modify button, scroll down to the "Connectivity" section, expand "Additonal configuration", choose "Publicly accessible" and then select the "Continue" button.

Now, when you select the name of your database instance in the Databases screen, you will be shown the database instance FQDN and port

![DB Public DNS](https://user-images.githubusercontent.com/9034190/120908115-346c2100-c635-11eb-8a06-0c471fd4473a.png)

#### Populate the Database Instance

For my testing I grabbed a [TMDB movie CSV](https://www.kaggle.com/tmdb/tmdb-movie-metadata) from Kaggle specifically, the "tmdb_5000_movies.csv" file. You can use any comma separated or tab separated file to populate your database (You need a free Kaggle account in order to download files).

![tmdb](https://user-images.githubusercontent.com/9034190/120908357-7a29e900-c637-11eb-8256-f0f9050f08bd.png)

![Spreadsheet](https://user-images.githubusercontent.com/9034190/120908599-cd9d3680-c639-11eb-998c-b912ccf9c56f.png)

OK, now that we have some data to populate our RDS database with, lets create a database, create a table and import the data. If you need a refresher on SQL syntax, check out the W3Schools [tutorial](https://www.w3schools.com/sql/)

* Connect to your RDS database instance with your mysql-client
````bash
mysql -h hello-mysql.c9kyvjbd9tpz.us-east-1.rds.amazonaws.com -P 3306 -u admin -p (use your FQDN)
````

* Create your database
````sql
create database dennis; (Call yours whatever you want)
show databases;
+--------------------+
| Database           |
+--------------------+
| dennis             |
| information_schema |
| mysql              |
| performance_schema |
+--------------------+
````

* Create your database table
````sql
Use dennis;

Create table imdb (Budget int(10), genres varchar(100), homepage varchar(100),	id int(10), keywords varchar(100),\
original_language varchar(2), original_title varchar(100), overview varchar(100), popularity decimal(9,6),\
production_companies varchar(100), production_countries varchar(100),  release_date date, revenue int(10),\
runtime int(3),	spoken_languages  varchar(100), status varchar(100), tagline varchar(100), title varchar(100),\
vote_average decimal(2,1), vote_count int(10));

describe imdb;
+----------------------+--------------+------+-----+---------+-------+
| Field                | Type         | Null | Key | Default | Extra |
+----------------------+--------------+------+-----+---------+-------+
| Budget               | int          | YES  |     | NULL    |       |
| genres               | varchar(100) | YES  |     | NULL    |       |
| homepage             | varchar(100) | YES  |     | NULL    |       |
| id                   | int          | YES  |     | NULL    |       |
| keywords             | varchar(100) | YES  |     | NULL    |       |
| original_language    | varchar(2)   | YES  |     | NULL    |       |
| original_title       | varchar(100) | YES  |     | NULL    |       |
| overview             | varchar(100) | YES  |     | NULL    |       |
| popularity           | decimal(9,6) | YES  |     | NULL    |       |
| production_companies | varchar(100) | YES  |     | NULL    |       |
| production_countries | varchar(100) | YES  |     | NULL    |       |
| release_date         | date         | YES  |     | NULL    |       |
| revenue              | int          | YES  |     | NULL    |       |
| runtime              | int          | YES  |     | NULL    |       |
| spoken_languages     | varchar(100) | YES  |     | NULL    |       |
| status               | varchar(100) | YES  |     | NULL    |       |
| tagline              | varchar(100) | YES  |     | NULL    |       |
| title                | varchar(100) | YES  |     | NULL    |       |
| vote_average         | decimal(2,1) | YES  |     | NULL    |       |
| vote_count           | int          | YES  |     | NULL    |       |
+----------------------+--------------+------+-----+---------+-------+
````
Two issues I want to point out here:
1) I should have named my table tmdb not imdb but I didn't :smile:
2) A few of these columns should actually be defined as JSON not varchar(100), but my import would not work when the columns were defined as JSON. Column type can be changed after import.

* Import your data

````bash
(From your mysql-client to enable data import)
GRANT SESSION_VARIABLES_ADMIN ON *.* TO 'admin'@'%';

(From your bash prompt)
mysqlimport --local --compress --user=admin --password=super-secret-password --host=hello-mysql.c9kyvjbd9tpz.us-east-1.rds.amazonaws.com\
--fields-terminated-by='^v^i' tmdb_5000_movies.txt

(From your mysql-client)
 select title, vote_average from imdb limit 10;
+------------------------------------------+--------------+
| title                                    | vote_average |
+------------------------------------------+--------------+
| Avatar                                   |          7.2 |
| Pirates of the Caribbean: At World's End |          6.9 |
| Spectre                                  |          6.3 |
| The Dark Knight Rises                    |          7.6 |
| John Carter                              |          6.1 |
| Spider-Man 3                             |          5.9 |
| Tangled                                  |          7.4 |
| Avengers: Age of Ultron                  |          7.3 |
| Harry Potter and the Half-Blood Prince   |          7.4 |
| Batman v Superman: Dawn of Justice       |          5.7 |
+------------------------------------------+--------------+

````

Three more issues I want to point out here:
1) I usually use the "LOAD DATA INFILE" syntax from the mysql-client to load data into tables, but I was having all sorts of permission problems. I switched from mysql-client to mysqlimport and had success
2) I opened tmdb_5000_movies.csv in Excel and saved as tab delimited to tmdb_5000_movies.txt. The commas in some of the movie fields can cause problems with immport, so tab delimited was safer. You'll see the ^v^i in the mysqlimport syntax above. To insert a TAB in your command line, press [CTRL]V then [CTRL]I.
3) Make sure you delete the column header row from your input file before import

### Create the Serverless Lambda Function

OK, we have a serverless database, we can connect to it, and we have inserted some data. Let's create a serverless database search function.

* From the AWS Management Console, select ""All services" and then "Lambda"

![image](https://user-images.githubusercontent.com/9034190/120943398-980d5180-c6fc-11eb-99de-7f9842556bad.png)

* Select "Create function"

![image](https://user-images.githubusercontent.com/9034190/120943747-d7d53880-c6fe-11eb-9478-32c327eb517c.png)

* Give your function a name and choose your preferred programming language and then select the "Create function" button

![image](https://user-images.githubusercontent.com/9034190/120943813-3c909300-c6ff-11eb-91da-b2ec13ce19d1.png)

(I no longer program for a living, so I did some testing with a Javascript tutorial but was finally successful using this Python [tutorial](https://kuharan.medium.com/mysql-aws-lambda-webapp-521b16458b93) as a base)

Once your basic function has been created, you will have some sample Python code created for you. Double click "lambda_function.py" to see that sample code.

![image](https://user-images.githubusercontent.com/9034190/120944011-51215b00-c700-11eb-8116-d0337447ec3c.png)

Here's the thing about writing your code in the Lambda editor - this is the best place to test your final code. The one caveat is that any external language libraries have to be uploaded as a ZIP file. You cannot install them directly here as you could say in an online Jupyter notebook. There is some value in testing your code locally on your personal machine, instaling externally libraries and then uploading to Lambda. I'll use that method here.

#### Test You Code on Your Local Machine

We can start with the lambda_function.py that AWS was nice enough to create for us and build from there.  Create a directory on your local machine and copy and paste the code from lambda.py to your own lambda.py

````bash
cd Documents
mkdir YayLambda
cd YayLambda
vi lambda_funtion.py (paste sample code in)
````

Now, let's add some code to test the connection to our RDS database. I learned this code from this blog post
````python
🕙 Tue 06-08 08:48 AM ❯ cat lambda_function.py
import json
import mysql.connector

def lambda_handler(event, context):
    # TODO implement
    conn = mysql.connector.connect(user='admin', password='SuperSecretPassword',
                                  host='hello-mysql.c9kyvjbd9tpz.us-east-1.rds.amazonaws.com',database='dennis')

    if conn:
        print ("Connected Successfully")
    else:
        print ("Connection Not Established")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
````

The json python library is standard in Lambda but the mysql library is not. We need to install the mysql library into our code directory for later upload to Lambda. I learned how to do that from the same [blog post](https://kuharan.medium.com/mysql-aws-lambda-webapp-521b16458b93) referenced above (but I replaced pymysql with mysql-connector). We do that with this command:

````bash
pip install mysql-connector -t .
[Output]
Collecting mysql-connector
  Using cached mysql-connector-2.2.9.tar.gz (11.9 MB)
Using legacy 'setup.py install' for mysql-connector, since package 'wheel' is not installed.
Installing collected packages: mysql-connector
    Running setup.py install for mysql-connector ... done
Successfully installed mysql-connector-2.2.9

 ls -l
total 16
-rw-r--r-- 1 dennis dennis  483 Jun  8 08:48 lambda_function.py
drwxr-xr-x 4 dennis dennis 4096 Jun  8 09:01 mysql
drwxr-xr-x 2 dennis dennis 4096 Jun  8 09:01 mysql_connector-2.2.9-py3.9.egg-info
drwxr-xr-x 5 dennis dennis 4096 Jun  8 09:01 mysqlx
````

I hacked lambda_function.py a little so that it would run locally and I could test my database connection and the sql-connector library. Success! Let;s do the rest of the edits right in the Lambda web page.

````bash
$ cp lambda_function.py local_function.py
$ vi local_function.py
$ cat local_function.py
import json
import mysql.connector

#def lambda_handler(event, context):
def main():
    # TODO implement
    conn = mysql.connector.connect(user='admin', password='SuperSecretPassword',
                                  host='hello-mysql.c9kyvjbd9tpz.us-east-1.rds.amazonaws.com',database='dennis')

    if conn:
        print ("Connected Successfully")
    else:
        print ("Connection Not Established")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

if __name__ == "__main__":
    main()
    
$ python local_function.py
Connected Successfully
````

#### Let's Upload This Mess to Lambda

You can create a Lambda function from a ZIP of a directory structure including your code and and external libraries. We have built that directory, so let's ZIP it up and upload to Lambda.

````bash
 pwd
/home/dennis/Documents/YayLambda

zip -r YayLambda.zip *
  adding: lambda_function.py (deflated 40%)
  adding: local_function.py (deflated 40%)
  adding: mysql/ (stored 0%)
  adding: mysql/connector/ (stored 0%)
  adding: mysql/connector/errorcode.py (deflated 68%)
  adding: mysql/connector/conversion.py (deflated 77%)
  adding: mysql/connector/connection_cext.py (deflated 75%)
  adding: mysql/connector/errors.py (deflated 70%)
  adding: mysql/connector/abstracts.py (deflated 75%)
  adding: mysql/connector/fabric/ (stored 0%)
  adding: mysql/connector/fabric/__init__.py (deflated 54%)
  adding: mysql/connector/fabric/__pycache__/ (stored 0%)
  adding: mysql/connector/fabric/__pycache__/balancing.cpython-39.pyc (deflated 52%)
  adding: mysql/connector/fabric/__pycache__/__init__.cpython-39.pyc (deflated 36%)
  adding: mysql/connector/fabric/__pycache__/caching.cpython-39.pyc (deflated 54%)
  adding: mysql/connector/fabric/__pycache__/connection.cpython-39.pyc (deflated 58%)
  adding: mysql/connector/fabric/balancing.py (deflated 63%)
  adding: mysql/connector/fabric/caching.py (deflated 71%)
  adding: mysql/connector/fabric/connection.py (deflated 77%)
  adding: mysql/connector/__init__.py (deflated 64%)
  adding: mysql/connector/constants.py (deflated 70%)
  adding: mysql/connector/utils.py (deflated 71%)
  adding: mysql/connector/cursor.py (deflated 80%)
  adding: mysql/connector/charsets.py (deflated 80%)
  adding: mysql/connector/authentication.py (deflated 68%)
  adding: mysql/connector/__pycache__/ (stored 0%)
  adding: mysql/connector/__pycache__/dbapi.cpython-39.pyc (deflated 47%)
  adding: mysql/connector/__pycache__/authentication.cpython-39.pyc (deflated 56%)
  adding: mysql/connector/__pycache__/pooling.cpython-39.pyc (deflated 58%)
  adding: mysql/connector/__pycache__/errorcode.cpython-39.pyc (deflated 61%)
  adding: mysql/connector/__pycache__/charsets.cpython-39.pyc (deflated 71%)
  adding: mysql/connector/__pycache__/network.cpython-39.pyc (deflated 54%)
  adding: mysql/connector/__pycache__/optionfiles.cpython-39.pyc (deflated 50%)
  adding: mysql/connector/__pycache__/version.cpython-39.pyc (deflated 26%)
  adding: mysql/connector/__pycache__/utils.cpython-39.pyc (deflated 58%)
  adding: mysql/connector/__pycache__/__init__.cpython-39.pyc (deflated 45%)
  adding: mysql/connector/__pycache__/protocol.cpython-39.pyc (deflated 54%)
  adding: mysql/connector/__pycache__/errors.cpython-39.pyc (deflated 57%)
  adding: mysql/connector/__pycache__/cursor_cext.cpython-39.pyc (deflated 60%)
  adding: mysql/connector/__pycache__/custom_types.cpython-39.pyc (deflated 40%)
  adding: mysql/connector/__pycache__/cursor.cpython-39.pyc (deflated 63%)
  adding: mysql/connector/__pycache__/conversion.cpython-39.pyc (deflated 59%)
  adding: mysql/connector/__pycache__/constants.cpython-39.pyc (deflated 57%)
  adding: mysql/connector/__pycache__/connection_cext.cpython-39.pyc (deflated 57%)
  adding: mysql/connector/__pycache__/abstracts.cpython-39.pyc (deflated 63%)
  adding: mysql/connector/__pycache__/catch23.cpython-39.pyc (deflated 41%)
  adding: mysql/connector/__pycache__/connection.cpython-39.pyc (deflated 61%)
  adding: mysql/connector/locales/ (stored 0%)
  adding: mysql/connector/locales/__init__.py (deflated 52%)
  adding: mysql/connector/locales/eng/ (stored 0%)
  adding: mysql/connector/locales/eng/__init__.py (deflated 45%)
  adding: mysql/connector/locales/eng/client_error.py (deflated 60%)
  adding: mysql/connector/locales/eng/__pycache__/ (stored 0%)
  adding: mysql/connector/locales/eng/__pycache__/client_error.cpython-39.pyc (deflated 54%)
  adding: mysql/connector/locales/eng/__pycache__/__init__.cpython-39.pyc (deflated 12%)
  adding: mysql/connector/locales/__pycache__/ (stored 0%)
  adding: mysql/connector/locales/__pycache__/__init__.cpython-39.pyc (deflated 37%)
  adding: mysql/connector/custom_types.py (deflated 49%)
  adding: mysql/connector/dbapi.py (deflated 55%)
  adding: mysql/connector/django/ (stored 0%)
  adding: mysql/connector/django/creation.py (deflated 74%)
  adding: mysql/connector/django/validation.py (deflated 69%)
  adding: mysql/connector/django/compiler.py (deflated 67%)
  adding: mysql/connector/django/schema.py (deflated 65%)
  adding: mysql/connector/django/__init__.py (stored 0%)
  adding: mysql/connector/django/introspection.py (deflated 76%)
  adding: mysql/connector/django/client.py (deflated 66%)
  adding: mysql/connector/django/__pycache__/ (stored 0%)
  adding: mysql/connector/django/__pycache__/validation.cpython-39.pyc (deflated 39%)
  adding: mysql/connector/django/__pycache__/introspection.cpython-39.pyc (deflated 56%)
  adding: mysql/connector/django/__pycache__/features.cpython-39.pyc (deflated 48%)
  adding: mysql/connector/django/__pycache__/creation.cpython-39.pyc (deflated 47%)
  adding: mysql/connector/django/__pycache__/client.cpython-39.pyc (deflated 40%)
  adding: mysql/connector/django/__pycache__/__init__.cpython-39.pyc (deflated 20%)
  adding: mysql/connector/django/__pycache__/base.cpython-39.pyc (deflated 55%)
  adding: mysql/connector/django/__pycache__/compiler.cpython-39.pyc (deflated 52%)
  adding: mysql/connector/django/__pycache__/schema.cpython-39.pyc (deflated 49%)
  adding: mysql/connector/django/__pycache__/operations.cpython-39.pyc (deflated 54%)
  adding: mysql/connector/django/operations.py (deflated 72%)
  adding: mysql/connector/django/features.py (deflated 62%)
  adding: mysql/connector/django/base.py (deflated 73%)
  adding: mysql/connector/network.py (deflated 78%)
  adding: mysql/connector/cursor_cext.py (deflated 78%)
  adding: mysql/connector/pooling.py (deflated 72%)
  adding: mysql/connector/protocol.py (deflated 78%)
  adding: mysql/connector/version.py (deflated 47%)
  adding: mysql/connector/catch23.py (deflated 59%)
  adding: mysql/connector/optionfiles.py (deflated 74%)
  adding: mysql/connector/connection.py (deflated 77%)
  adding: mysql/__init__.py (stored 0%)
  adding: mysql/__pycache__/ (stored 0%)
  adding: mysql/__pycache__/__init__.cpython-39.pyc (deflated 23%)
  adding: mysql_connector-2.2.9-py3.9.egg-info/ (stored 0%)
  adding: mysql_connector-2.2.9-py3.9.egg-info/SOURCES.txt (deflated 78%)
  adding: mysql_connector-2.2.9-py3.9.egg-info/top_level.txt (deflated 8%)
  adding: mysql_connector-2.2.9-py3.9.egg-info/dependency_links.txt (stored 0%)
  adding: mysql_connector-2.2.9-py3.9.egg-info/PKG-INFO (deflated 59%)
  adding: mysql_connector-2.2.9-py3.9.egg-info/installed-files.txt (deflated 87%)
  adding: mysqlx/ (stored 0%)
  adding: mysqlx/compat.py (deflated 52%)
  adding: mysqlx/errorcode.py (deflated 68%)
  adding: mysqlx/errors.py (deflated 69%)
  adding: mysqlx/expr_unparser.py (deflated 67%)
  adding: mysqlx/crud.py (deflated 80%)
  adding: mysqlx/__init__.py (deflated 69%)
  adding: mysqlx/constants.py (deflated 50%)
  adding: mysqlx/charsets.py (deflated 80%)
  adding: mysqlx/authentication.py (deflated 56%)
  adding: mysqlx/__pycache__/ (stored 0%)
  adding: mysqlx/__pycache__/expr_unparser.cpython-39.pyc (deflated 46%)
  adding: mysqlx/__pycache__/statement.cpython-39.pyc (deflated 70%)
  adding: mysqlx/__pycache__/authentication.cpython-39.pyc (deflated 48%)
  adding: mysqlx/__pycache__/expr.cpython-39.pyc (deflated 55%)
  adding: mysqlx/__pycache__/errorcode.cpython-39.pyc (deflated 61%)
  adding: mysqlx/__pycache__/charsets.cpython-39.pyc (deflated 71%)
  adding: mysqlx/__pycache__/crud.cpython-39.pyc (deflated 71%)
  adding: mysqlx/__pycache__/__init__.cpython-39.pyc (deflated 54%)
  adding: mysqlx/__pycache__/protocol.cpython-39.pyc (deflated 54%)
  adding: mysqlx/__pycache__/errors.cpython-39.pyc (deflated 53%)
  adding: mysqlx/__pycache__/result.cpython-39.pyc (deflated 62%)
  adding: mysqlx/__pycache__/compat.cpython-39.pyc (deflated 34%)
  adding: mysqlx/__pycache__/dbdoc.cpython-39.pyc (deflated 43%)
  adding: mysqlx/__pycache__/constants.cpython-39.pyc (deflated 34%)
  adding: mysqlx/__pycache__/connection.cpython-39.pyc (deflated 60%)
  adding: mysqlx/locales/ (stored 0%)
  adding: mysqlx/locales/__init__.py (deflated 53%)
  adding: mysqlx/locales/eng/ (stored 0%)
  adding: mysqlx/locales/eng/__init__.py (stored 0%)
  adding: mysqlx/locales/eng/client_error.py (deflated 60%)
  adding: mysqlx/locales/eng/__pycache__/ (stored 0%)
  adding: mysqlx/locales/eng/__pycache__/client_error.cpython-39.pyc (deflated 54%)
  adding: mysqlx/locales/eng/__pycache__/__init__.cpython-39.pyc (deflated 21%)
  adding: mysqlx/locales/__pycache__/ (stored 0%)
  adding: mysqlx/locales/__pycache__/__init__.cpython-39.pyc (deflated 37%)
  adding: mysqlx/protobuf/ (stored 0%)
  adding: mysqlx/protobuf/mysqlx_session_pb2.py (deflated 82%)
  adding: mysqlx/protobuf/mysqlx_sql_pb2.py (deflated 73%)
  adding: mysqlx/protobuf/mysqlx_connection_pb2.py (deflated 81%)
  adding: mysqlx/protobuf/__init__.py (stored 0%)
  adding: mysqlx/protobuf/mysqlx_datatypes_pb2.py (deflated 86%)
  adding: mysqlx/protobuf/mysqlx_expr_pb2.py (deflated 87%)
  adding: mysqlx/protobuf/__pycache__/ (stored 0%)
  adding: mysqlx/protobuf/__pycache__/mysqlx_notice_pb2.cpython-39.pyc (deflated 57%)
  adding: mysqlx/protobuf/__pycache__/mysqlx_resultset_pb2.cpython-39.pyc (deflated 59%)
  adding: mysqlx/protobuf/__pycache__/mysqlx_crud_pb2.cpython-39.pyc (deflated 66%)
  adding: mysqlx/protobuf/__pycache__/mysqlx_connection_pb2.cpython-39.pyc (deflated 54%)
  adding: mysqlx/protobuf/__pycache__/mysqlx_session_pb2.cpython-39.pyc (deflated 55%)
  adding: mysqlx/protobuf/__pycache__/mysqlx_datatypes_pb2.cpython-39.pyc (deflated 61%)
  adding: mysqlx/protobuf/__pycache__/t.cpython-39.pyc (deflated 12%)
  adding: mysqlx/protobuf/__pycache__/mysqlx_pb2.cpython-39.pyc (deflated 57%)
  adding: mysqlx/protobuf/__pycache__/mysqlx_sql_pb2.cpython-39.pyc (deflated 48%)
  adding: mysqlx/protobuf/__pycache__/__init__.cpython-39.pyc (deflated 21%)
  adding: mysqlx/protobuf/__pycache__/mysqlx_expr_pb2.cpython-39.pyc (deflated 63%)
  adding: mysqlx/protobuf/__pycache__/mysqlx_expect_pb2.cpython-39.pyc (deflated 52%)
  adding: mysqlx/protobuf/mysqlx_crud_pb2.py (deflated 89%)
  adding: mysqlx/protobuf/mysqlx_expect_pb2.py (deflated 79%)
  adding: mysqlx/protobuf/t.py (deflated 46%)
  adding: mysqlx/protobuf/mysqlx_notice_pb2.py (deflated 83%)
  adding: mysqlx/protobuf/mysqlx_pb2.py (deflated 82%)
  adding: mysqlx/protobuf/mysqlx_resultset_pb2.py (deflated 84%)
  adding: mysqlx/protocol.py (deflated 76%)
  adding: mysqlx/dbdoc.py (deflated 52%)
  adding: mysqlx/result.py (deflated 77%)
  adding: mysqlx/expr.py (deflated 78%)
  adding: mysqlx/statement.py (deflated 81%)
  adding: mysqlx/connection.py (deflated 75%)
  
````

Now we can upload YayLambda.zip to AWS Lambda

* From our Lambda Code source windows, select Upload from > .zip file

![image](https://user-images.githubusercontent.com/9034190/121270126-1ac61600-c88f-11eb-9a2a-c72aa4ef9c23.png)

* Select the Upload button, choose your ZIP file and then select the Save button

![image](https://user-images.githubusercontent.com/9034190/121270255-58c33a00-c88f-11eb-8e4f-ef8843a30b73.png)

![image](https://user-images.githubusercontent.com/9034190/121270536-e9017f00-c88f-11eb-8567-b418b0bdea4b.png)

We now have our starter code and all the libraries we need in our Lambda function.

![image](https://user-images.githubusercontent.com/9034190/121270743-472e6200-c890-11eb-89e5-c4c426285def.png)

#### Test our start code with an event

Lambda functions are triggered by events. We can create a test event and see if our code is working in AWS.

* Select Test and then Configure test event

![image](https://user-images.githubusercontent.com/9034190/121271150-100c8080-c891-11eb-89c9-0b347462b0af.png)

* Use the defaults, give your event a name and select the Create button

![image](https://user-images.githubusercontent.com/9034190/121271966-d177c580-c892-11eb-92e0-e802bc3be11c.png)

Now before we test our code, I want to point out something important I learned through trial and error (and error). There is a Runtime settings section below your code that specifies the name of the file and the name of the function that will be run. Make sure this matches you code.

![image](https://user-images.githubusercontent.com/9034190/121272101-1e5b9c00-c893-11eb-8b4e-0c074bcaffa2.png)

To test our code with our new test event just select the "Test" button. You will see the JSON output of lambda_function.py in the Execution results tab

![image](https://user-images.githubusercontent.com/9034190/121272371-c8d3bf00-c893-11eb-8eb5-9aa4988823ea.png)

#### Test Our Code on the Web

We haven't added our beautiful SQL statements yet to our code, but being able to call this function from a web page is so cool, let's do that now and then come back and add the SQL statements.

* From Function overview select the "Add trigger" button

![image](https://user-images.githubusercontent.com/9034190/121273052-57950b80-c895-11eb-8dd0-575d21f095c2.png)


* Select "API Gateway", "Create an API", Open Security, and then the "Add" buttion.

![image](https://user-images.githubusercontent.com/9034190/121273233-c5413780-c895-11eb-80a0-ffd4cd1443b5.png)

An API gateway will be created with a public URL

![image](https://user-images.githubusercontent.com/9034190/121422347-24a65280-c93d-11eb-81a2-24e59f4625ab.png)

If we visit that public URL, something should happen

![image](https://user-images.githubusercontent.com/9034190/121422597-646d3a00-c93d-11eb-9bbc-4f7a43529dd3.png)

#### Add a Custom SQL Select Statement to our Code

Now that we know that our Lambda function can be triggered by visiting a web page, let's add some code to accept a value in the URL and search for that value in our database.

Here is the code that worked for me. I will provide explanation as comments in the code listing. I have also uploaded my final code to this repo. Be kind, I no longer code for a living :smile: 

````Python
import mysql.connector  # Import the MySQL Library we uploaded
import json             # For JSON handling. DO not need to upload this library
import re               # To prevent SQL Injection my cleaning the input variable

def lambda_handler(event, context):              # This is important and Lambda is looking for "lambda_handler"
                                                 # The next line connects to our RDS MySQL database
    conn = mysql.connector.connect(user='admin', password='SuperSecretPassword',
                                  host='hello-mysql.c9kyvjbd9tpz.us-east-1.rds.amazonaws.com',database='dennis')
    
    if conn:                                     # Check for a successful database connection
        print ("Connected Successfully")
    else:
        print ("Connection Not Established")
    
    class create_dict(dict):                     # Create a structure to hold the results of our SQL query. There may be a better way.
      
        # __init__ function 
        def __init__(self): 
            self = dict() 
              
        # Function to add key:value 
        def add(self, key, value): 
            self[key] = value
    
    mydict = create_dict()                       # Initialize our dict structure
    movie_name = event['queryStringParameters']['movie_name']        # Get the movie_name string passed in the URL as ?movie_name="Name"
    clean_movie = re.sub('[^A-Za-z0-9 ]+', '', movie_name)           # Use the re library to strip nasty SQL Inject characters 
                                                                     # The next line is our SQL SELECT statement using the passed variable
    select_movie = "select title,popularity,vote_average from dennis.imdb where title like \"" + clean_movie + "%\"  order by popularity desc"
    cursor = conn.cursor()
    cursor.execute(select_movie)                                     # Send the SELECT statement
    result = cursor.fetchall()                                       # Get the results
    
    for row in result:                                               # Loop through the rows returned, adding them to a python structure
        mydict.add(row[0],({"popularity":str(row[1]),"vote_average":str(row[2])}))
    
    movie_json = json.dumps(mydict, indent=2)        # Convert python object to JSON string, indents the JSON 
    
    return movie_json

````

Now, when we append something like ?movie_name="Star" to our Web API URL, we get a list of movies starting with "Star" sortted by popularity

![image](https://user-images.githubusercontent.com/9034190/121428837-40f9bd80-c944-11eb-8ccb-0221cfc81ca0.png)


## Thank you

Thank you for taking the time to reasd this _long_ post. I could not find any other blog posts that did exactly this or were written in a way that I could understand. I hope you found this helpful, educational, and easy to understand. I welcome your feedback.
