from pymongo import MongoClient
def get_db():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb://localhost/"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['flask']
  
# This is added so that many files can reuse the function get_db()
if __name__ == "__main__":   
  
   # Get the database
   dbname = get_db()
