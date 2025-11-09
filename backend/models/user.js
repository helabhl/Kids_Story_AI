const mongoose = require("mongoose");

const UserSchema = new mongoose.Schema({
  user_id: { type: String, required: true, unique: true },
  age: Number,
  age_range: String, // ex "6-8", "9-12"
  preferred_genres: [String],
  preferred_characters: [String],
  preferred_emotions: [String],
  preferred_reading_time: Number, // en minutes préférés
  reading_time_min: Number,
  reading_time_max: Number,
  stories_per_week: Number,
  activity_level: { type: String, enum: ["low","medium","high"], default: "medium" },
  prefers_illustrations: { type: Boolean, default: true },
  prefers_interactive_questions: { type: Boolean, default: false },
  registration_date: Date,
  favorite_genre: String,
  total_likes: { type: Number, default: 0 },
  total_completed: { type: Number, default: 0 },
  total_stories_read: { type: Number, default: 0 },
  total_reading_time_minutes: { type: Number, default: 0 }
}, { timestamps: true });

module.exports = mongoose.model("User", UserSchema);
