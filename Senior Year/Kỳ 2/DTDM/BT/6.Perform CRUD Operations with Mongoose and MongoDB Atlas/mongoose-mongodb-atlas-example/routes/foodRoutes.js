const express = require("express");
const foodModel = require("../models/food");
const router = express.Router(); // Đổi từ app sang router

// GET all foods
router.get("/foods", async (req, res) => {
  try {
    const foods = await foodModel.find({});
    res.send(foods);
  } catch (error) {
    res.status(500).send(error);
  }
});

// POST new food
router.post("/food", async (req, res) => {
  try {
    const food = new foodModel(req.body);
    await food.save();
    res.send(food);
  } catch (error) {
    res.status(500).send(error);
  }
});

// PATCH update food (FIXED)
router.patch("/food/:id", async (req, res) => {
  try {
    const food = await foodModel.findByIdAndUpdate(
      req.params.id,
      req.body,
      { new: true } // Trả về document đã update
    );
    if (!food) return res.status(404).send("Not found");
    res.send(food);
  } catch (error) {
    res.status(500).send(error);
  }
});

router.delete("/food/:id", async (request, response) => {
try {
const food = await foodModel.findByIdAndDelete(request.params.id);
if (!food) response.status(404).send("No item found");
response.status(200).send();
} catch (error) {
response.status(500).send(error);
}
});

module.exports = router; // Xuất router thay vì app
