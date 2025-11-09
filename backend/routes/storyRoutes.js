const express = require("express");
const { getAllStories, getStoryById,createStory } = require("../controllers/storyController");

const router = express.Router();

router.get("/", getAllStories);
router.get("/:id", getStoryById);
router.post("/", createStory); // <-- Route POST pour créer une story


module.exports = router;
