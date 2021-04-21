# dataIngestion
firstly I have scrapped the 5000 github repositories getting data Repo Url,Repo id,Repo Name,Repo rank by using the beautiful soap library,after getting this data ,I am saving this data into acsv file named as reposs.csv.
Secondly I am getting Github Repositories data by using the Github API,after getting the response i am sending this data to postgre SQL database bu using the libarary psycopg2.
There were making 7 different tables in in the database .
