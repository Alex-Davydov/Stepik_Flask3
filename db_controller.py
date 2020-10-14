import json
import os


def loader(db_name):
    with open('.'.join((db_name, 'json')), 'r') as db:
        teachers_data = json.load(db)
        return teachers_data


def db_manager(db_name, data):
    if not os.path.exists('.'.join((db_name, 'json'))):
        with open('.'.join((db_name, 'json')), 'w') as db:
            json.dump(data, db)
    else:
        with open('.'.join((db_name, 'json')), 'r+') as db:
            current_db = json.load(db)
            current_db.extend(data)
            db.seek(0)
            json.dump(current_db, db)
