"""One-time script to clean HTML artifacts from all stored sentiment text."""
import sys, re
sys.path.insert(0, '.')
from database.mongo_client import Database

db = Database()
count = 0

for doc in db.sentiments.find():
    t = doc.get('text', '')
    if not t:
        continue
    clean = re.sub(r'&nbsp;', ' ', t)
    clean = re.sub(r'[A-Za-z0-9_\-]{60,}', '', clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    if clean != t:
        db.sentiments.update_one({'_id': doc['_id']}, {'$set': {'text': clean}})
        count += 1

print(f'Cleaned {count} records')
