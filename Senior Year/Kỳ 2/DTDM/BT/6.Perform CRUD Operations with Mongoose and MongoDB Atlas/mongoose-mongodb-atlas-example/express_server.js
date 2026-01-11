const express = require("express");
const mongoose = require("mongoose");
const methodOverride = require('method-override');
const foodRouter = require("./routes/foodRoutes.js");

const app = express();
app.use(methodOverride('_method'));
app.use(express.json());

// Kết nối MongoDB Atlas với xử lý lỗi đầy đủ
async function connectToDatabase() {
  try {
    await mongoose.connect(
      "mongodb+srv://phucan2370:bPGZKpdWkPiSLUKW@cluster0.is0wdhq.mongodb.net/foodDB?retryWrites=true&w=majority",
      {
        useNewUrlParser: true,
        useUnifiedTopology: true,
        serverSelectionTimeoutMS: 5000, // Timeout sau 5 giây nếu không kết nối được
        ssl: true // Bắt buộc với MongoDB Atlas
      }
    );
    console.log("✅ Connected to MongoDB Atlas");
  } catch (err) {
    console.error("❌ MongoDB connection error:", err);
    process.exit(1); // Thoát ứng dụng nếu không kết nối được
  }
}

connectToDatabase();

// Xử lý sự kiện kết nối
mongoose.connection.on("connected", () => {
  console.log("Mongoose connected to DB");
});

mongoose.connection.on("error", (err) => {
  console.error("Mongoose connection error:", err);
});

app.use(foodRouter);

app.listen(3000, () => {
  console.log("🚀 Server is running on http://localhost:3000");
});
