const Story = require("../models/story");

// ✅ GET all stories
// GET /api/stories?page=1&limit=10
const getAllStories = async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1; // page courante
    const limit = parseInt(req.query.limit) || 10; // nombre de stories par page
    const skip = (page - 1) * limit;

    const totalStories = await Story.countDocuments();
    const stories = await Story.find()
      .skip(skip)
      .limit(limit)
      .sort({ createdAt: -1 }); // les plus récentes d'abord

    res.json({
      page,
      limit,
      totalStories,
      totalPages: Math.ceil(totalStories / limit),
      stories
    });
  } catch (error) {
    res.status(500).json({ message: "Erreur lors de la récupération des stories", error });
  }
};


// ✅ GET one story by ID
const getStoryById = async (req, res) => {
  try {
    const story = await Story.findById(req.params.id);
    if (!story) {
      return res.status(404).json({ message: "Story non trouvée" });
    }
    res.status(200).json(story);
  } catch (error) {
    res.status(500).json({ message: "Erreur serveur", error });
  }
};

// ✅ Créer une nouvelle story
const createStory = async (req, res) => {
  console.log(req.body); // 🔍 voir ce que le serveur reçoit
  try {
    const {
      story_id,
      title,
      genre,
      tags,
      reading_time,
      views,
      likes,
      text,
      questions,
      url,
      image_url
    } = req.body;

    const newStory = new Story({
      story_id,
      title,
      genre,
      tags,
      reading_time,
      views: views || 0,
      likes: likes || 0,
      text,
      questions,
      url,
      image_url
    });

    const savedStory = await newStory.save();
    res.status(201).json(savedStory);
  } catch (error) {
    res.status(500).json({ message: "Erreur lors de la création de la story", error });
  }
};


module.exports = { getAllStories, getStoryById, createStory };