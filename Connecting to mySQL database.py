import pyodbc
server = 'location' #eg.scrapersmsda2017.database.windows.net
database = 'datbasename' #eg. msdatwitter
username = 'usename' 
password = 'password'
driver= '{ODBC Driver 17 for SQL Server}' #can change depending on your driver 
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

#test query
#this is only for Microsoft Azure test tables for MSDA project 
cursor.execute("SELECT TOP 20 pc.Name as CategoryName, p.name as ProductName FROM [SalesLT].[ProductCategory] pc JOIN [SalesLT].[Product] p ON pc.productcategoryid = p.productcategoryid")
row = cursor.fetchone()
while row:
   print (str(row[0]) + " " + str(row[1]))
   row = cursor.fetchone()
