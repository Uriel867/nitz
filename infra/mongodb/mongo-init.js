db = db.getSiblingDB('lol');
db.createCollection('summoners');
db.createCollection('matches');
console.log("Database and collection initialized successfully!");
