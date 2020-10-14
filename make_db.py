import json


from data import teachers


with open('teachers.json', 'w') as db:
    json.dump(teachers, db)
