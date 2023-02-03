const mongoose = require("mongoose");

const userSchema = new mongoose.Schema(
  {
    userId: { type: String, unique: true, required: true },
    password: { type: String, required: true },
    hood: [Number],
    knit: [Number],
    long: [Number],
    polo: [Number],
    shirt: [Number],
    short: [Number],
    sleeveless: [Number],
    sweat: [Number],
    cotton: [Number],
    denim: [Number],
    jogger: [Number],
    jumper: [Number],
    leggings: [Number],
    shorts: [Number],
    slacks: [Number],
    etc: [Number],
  },
  { timestamps: true, collection: "users" }
);

const User = mongoose.model("User", userSchema);

module.exports = { User };
