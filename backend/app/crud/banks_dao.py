from backend.app.database import banks_accounts_collection as db



def create(name, port):
    db.insert_one({"name": name, "port": port})
