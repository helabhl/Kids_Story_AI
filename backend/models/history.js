const mongoose = require("mongoose");

const HistorySchema = new mongoose.Schema({
  history_id: { type: String, required: true, unique: true },
  user_id: { type: String, required: true, index: true },
  story_id: { type: String, required: true, index: true },
  session_id: String,
  read_date: { type: Date, default: Date.now },
  reading_progress: { type: Number, min: 0, max: 100 }, // % read
  completed: { type: Boolean, default: false },
  time_spent_minutes: { type: Number, default: 0 },
  liked: { type: Boolean, default: false },
  rating: { type: Number, min: 0, max: 5 },
  added_to_favorites: { type: Boolean, default: false },
  shared: { type: Boolean, default: false },
  answered_questions: { type: Number, default: 0 },
  questions_correct: { type: Number, default: 0 },
  device_type: String // "mobile", "desktop", "tablet"
}, { timestamps: true });

module.exports = mongoose.model("History", HistorySchema);
