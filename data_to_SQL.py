import pandas as pd
import pyodbc

data = pd.read_csv(r'repos.csv')
df = pd.DataFrame(data, columns=['Repo_URL', 'Repo_Name', 'Repo_ID', 'Rating', 'Repo_Rank'])
# print('df: ', df)
# Connect to SQL Server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-H41J73T\SQLEXPRESS;'
                      'Database=test;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

# Create Table
cursor.execute(
    'CREATE TABLE repos (Repo_URL nvarchar(200), Repo_Name nvarchar(200), Repo_ID int,Rating int,Repo_Rank int  )')

# Insert DataFrame to Table
count  = 0
for row in df.itertuples():
    count += 1
    print('Counter: ',count)
    cursor.execute('''
                INSERT INTO dbo.repos (Repo_URL, Repo_Name, Repo_ID,Rating,Repo_Rank )
                VALUES (?,?,?,?,?)
                ''',
                row.Repo_URL,
                row.Repo_Name,
                row.Repo_ID,
                row.Rating,
                row.Repo_Rank
                )
    print(row.Repo_URL)
conn.commit()
# cursor.execute('''
#                 INSERT INTO dbo.people_info (Name, Country, Age)
#                 VALUES (?,?,?)
#                 ''',
#                 'Muhammad Ahmed',
#                 'Pakistan',
#                 '45'
#                 )
#
# conn.commit()
