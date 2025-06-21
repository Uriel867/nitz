db = db.getSiblingDB('testdb');
db.createCollection('users');
db.users.insertOne({ name: "Alice", age: 30, email: "alice@example.com" });
db.users.insertOne({ name: "Bob", age: 25, email: "bob@example.com" });
console.log("Database and collection initialized successfully!");
