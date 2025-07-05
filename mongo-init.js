db = db.getSiblingDB('testdb');
db.createCollection('summoners');
db.createCollection('match');
db.createCollection('matchID');
console.log("Database and collection initialized successfully!");
