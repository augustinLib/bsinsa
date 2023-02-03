const mongoose = require("mongoose");

const itemSchema = new mongoose.Schema(
  {
    _id: mongoose.Schema.Types.ObjectId,
    brand: "string",
    category: "string",
    brand: "string",
    like: "string",
    price: "string",
    product_name: "string",
    product_num: "number",
    rate: "string",
    tag: "string",
    year_sold: "string",
  },
  { timestamps: true, collection: "item" }
);

const Item = mongoose.model("Item", itemSchema);

module.exports = { Item };
