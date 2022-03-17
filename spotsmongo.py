import os
import pymongo

mongo_pass = os.environ['MONGO_PASS']
client = pymongo.MongoClient(f"mongodb+srv://bot-api:{mongo_pass}@cluster0.7yqyv.mongodb.net/telegram?retryWrites=true&w=majority")
db = client["telegram"]
collection = db["bot-kgv"]

def save(update):
    message = update.message.text
    tmp = message[9:].split('_at_')
    date = tmp[0].replace('_', '/')
    time = tmp[1].replace('_', ':')

    data = {}
    data['chat_id'] = update.message.chat_id
    data['date'] = date
    data['time'] = time
    
    collection.insert_one(data)

def list(update):
    commands = ''
    spots = collection.find({"chat_id": update.message.chat_id})
    for spot in spots:
        try:
            full_command = f'/remove_{spot["date"].replace("/", "_")}_at_{spot["time"].replace(":", "_")}\n'
            commands += full_command
        except:
            pass
    
    return commands

def remove(update):
    message = update.message.text
    tmp = message[8:].split('_at_')
    date = tmp[0].replace('_', '/')
    time = tmp[1].replace('_', ':')
    doc = collection.find_one({'$and': [{"chat_id": update.message.chat_id}, {"date": date}, {"time": time}]})
    if doc:
        return collection.delete_one(doc)
