const { MongoClient } = require("mongodb");

// Connect to MongoDB
const url = "mongodb://localhost:27017/";
const client = new MongoClient(url);

async function main() {
    try {
        await client.connect();
        console.log("Connected to MongoDB successfully!");

        const db = client.db("test");
        const collection = db.collection("users");

        // Ensure no duplicate insertions
        await collection.deleteMany({}); // Clears the collection before inserting

        // Insert data into the collection
        let data = [
            { id: 100, name: "An Phúc", age: 24 },
            { id: 101, name: "Khải", age: 25 },
            { id: 102, name: "Thi", age: 30 },
            { id: 103, name: "Khánh", age: 28 }
        ];
        await collection.insertMany(data);
        console.log("Data has been inserted!");

        // Retrieve data
        let user = await collection.findOne({ id: 100 });
        if (user) {
            console.log("Retrieved record:", user);
        } else {
            console.log("Record with id: 100 not found.");
        }

        // Update data only if it exists
        const updateResult = await collection.updateOne(
            { id: 100 },
            { $set: { age: 26 } }
        );
        if (updateResult.matchedCount > 0) {
            console.log("Data has been updated!");
        } else {
            console.log("No matching record found for update.");
        }

        // Delete data safely
        const deleteResult = await collection.deleteOne({ id: 102 });
        if (deleteResult.deletedCount > 0) {
            console.log("A record has been deleted!");
        } else {
            console.log("No matching record found for deletion.");
        }

        // Sort and display the user list
        let sortedUsers = await collection.find().sort({ age: 1 }).toArray();
        console.log("Sorted user list by age:", sortedUsers);
    } catch (error) {
        console.error("Error:", error);
    } finally {
        await client.close();
        console.log("Connection to MongoDB has been closed.");
    }
}

// Run the main function
main();
