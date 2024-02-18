from ZODB import FileStorage, DB
import transaction

# Open the database file storage
storage = FileStorage.FileStorage('db/testdb.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

# Example of deleting items
for key in list(root.keys()):
    del root[key]
transaction.commit()

# Add an item to the root object
root[175369] = {"name": "Atomic Ant", "rank": 1}
root[393346] = {"name": "Butanic", "rank": 2}
transaction.commit()

# Print out all items in the database
for key, value in root.items():
    print(f"Key: {key}, Value: {value}")

# Close the database connection
connection.close()
db.close()
