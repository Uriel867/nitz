db = db.getSiblingDB('lol');
db.createCollection('summoners');
db.createCollection('match_data');
db.createCollection('match_id');
console.log("Database and collection initialized successfully!");
