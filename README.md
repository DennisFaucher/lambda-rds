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


### Create the Serverless Lambda Function
## Thank you
