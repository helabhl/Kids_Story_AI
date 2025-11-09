const History = require("../models/history");

// ✅ GET all histories
const getAllHistory = async (req, res) => {
  try {
    const history = await History.find();
    res.status(200).json(history);
  } catch (error) {
    res.status(500).json({ message: "Erreur serveur", error });
  }
};

// ✅ GET history by user
const getHistoryByUser = async (req, res) => {
  try {
    const userHistory = await History.find({ user_id: req.params.user_id });
    res.status(200).json(userHistory);
  } catch (error) {
    res.status(500).json({ message: "Erreur serveur", error });
  }
};

module.exports = { getAllHistory, getHistoryByUser };
