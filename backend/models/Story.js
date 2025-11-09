const mongoose = require("mongoose");

const storySchema = new mongoose.Schema({
  story_id: { type: String, required: true, unique: true },
  title: { type: String, required: true },
  genre: String,
  tags: [String],
  reading_time: Number,
  views: { type: Number, default: 0 },
  likes: { type: Number, default: 0 },
  text: String,
  questions: [String],
  url: String,
  image_url: String,
}, { timestamps: true, collection: "Story" }); // ✅ tout dans un seul objet

module.exports = mongoose.model("Story", storySchema);
