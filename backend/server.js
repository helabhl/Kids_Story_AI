const express = require("express");
const mongoose = require("mongoose");
const dotenv = require("dotenv");

const storyRoutes = require("./routes/storyRoutes");
const userRoutes = require("./routes/userRoutes");
const historyRoutes = require("./routes/historyRoutes");

dotenv.config();

const app = express();
app.use(express.json());

const cors = require("cors");
app.use(cors()); // Permet au frontend React d'accéder au backend


// Connexion à MongoDB
mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log("✅ MongoDB connecté"))
  .catch(err => console.error("❌ Erreur MongoDB:", err));

// Routes principales
app.use("/api/stories", storyRoutes);
app.use("/api/users", userRoutes);
app.use("/api/history", historyRoutes);

// Lancement du serveur
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`🚀 Serveur lancé sur le port ${PORT}`));
