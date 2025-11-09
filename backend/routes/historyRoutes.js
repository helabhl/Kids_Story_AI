const express = require("express");
const { getAllHistory, getHistoryByUser } = require("../controllers/historyController");

const router = express.Router();

router.get("/", getAllHistory);
router.get("/user/:user_id", getHistoryByUser);

module.exports = router;
