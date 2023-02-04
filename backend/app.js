var express = require("express");
var path = require("path");
const cors = require("cors");
const session = require("express-session");
const MemoryStore = require("memorystore")(session);
const mongoose = require("mongoose");
const axios = require("axios");
const bodyParser = require("body-parser");
const { User } = require("./Model/User");

var app = express();

app.use(cors());
app.use(express.static(path.join(__dirname, "../frontend/build")));
app.use(bodyParser.json());
app.use(
  session({
    secret: "MySecret",
    resave: false,
    saveUninitialized: true,
    store: new MemoryStore({}),
    cookie: { maxAge: 86400000 },
  })
);

app.use(express.urlencoded({ extended: true }));

app.get("/api", (req, res) => {
  const { Item } = require("./Model/Image");
  Item.find()
    .limit(10)
    .then((data) => {
      res.json(data);
    })
    .catch((err) => {
      console.log("Error: ", err);
    });
});

app.get("/api/home-data", (req, res) => {
  axios
    .get("http://0.0.0.0:8001/home-data")
    .then((response) => res.json(response.data))
    .catch((error) => res.json({ error: error.message }));
});

app.get("/api/item-data/:id", (req, res) => {
  axios
    .get("http://0.0.0.0:8001/item/" + req.params.id)
    .then((response) => res.json(response.data))
    .catch((error) => res.json({ error: error.message }));
});

app.get("/api/category-data/:id", (req, res) => {
  axios
  .get("http://0.0.0.0:8001/product-data/" + req.params.id)
  .then((response) => res.json(response.data))
  .catch((error) => res.json({ error: error.message }));
})

app.get("/api/initial-data", (req, res) => {
  axios
    .get("http://0.0.0.0:8001/initial-data")
    .then((response) => res.json(response.data))
    .catch((error) => res.json({ error: error.message }));
});

app.post("/api/register", (req, res) => {
  const temp = { userId: req.body.id, password: req.body.password };
  const NewUser = new User(temp);
  NewUser.save((err, savedForm) => {
    if (err) {
      if (err.code === 11000) {
        res.status(501).send(err);
        console.log(err.name);
        console.log(err.code);
      } else {
        res.status(500).send(err);
      }
    } else {
      res.status(200).send(savedForm);
    }
  });
});

app.post("/api/login", (req, res) => {
  const { id, password } = req.body;
  User.findOne({ userId: id }, (err, user) => {
    if (err) {
      console.log(err);
    } else {
      if (user) {
        if (user.password === password) {
          req.session.user = user.userId;
          res.status(200).send("Success!");
        } else {
          res.status(502).send("Wrong password");
        }
      } else {
        res.status(503).send("User not found");
      }
    }
  });
});

app.get("/api/logout", (req, res) => {
  req.session.destroy(() => req.session);
  res.status(200).send("Logged out");
  console.log("Logged out");
  console.log("Session: ", req.session);
});

app.get("/api/check-login", (req, res) => {
  if (req.session.user) {
    res.status(200).json({ isLoggedIn: true });
    console.log("Logged in");
  } else {
    res.status(500).json({ isLoggedIn: false });
  }
});

app.get("/api/user", (req, res) => {
  if (req.session.user) {
    User.findOne({ userId: req.session.user }, (err, user) => {
      if (err) {
        console.log(err);
      } else {
        if (user) {
          res.status(200).json({ user: user });
        } else {
          res.status(503).send("User not found");
        }
      }
    });
  } else {
    res.status(500).json({ isLoggedIn: false });
  }
});

app.post("/api/likes", (req, res) => {
  const { userId, liked } = req.body;
  for (const key in liked) {
    liked[key].map((item) => {
      User.findOneAndUpdate(
        { userId: userId },
        { $addToSet: { [key]: item } },
        (err, user) => {
          if (err) {
            console.log(err);
          } else {
            if (user) {
              console.log("Liked", item);
            } else {
              res.status(503).send("User not found");
            }
          }
        }
      );
    });
  }
});

app.get("*", function (req, res) {
  res.sendFile(path.join(__dirname, "../frontend/build", "index.html"));
});
// 125.128.172.226

app.listen(3000, "0.0.0.0", () => {
  console.log("Server started on port 3000");
  console.log(path.join(__dirname, "../frontend/build/index.html"));
});

mongoose
  .connect("mongodb://localhost:27017/conference", {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => {
    console.log("Connected to MongoDB!!!");
  })
  .catch((err) => {
    console.log("Error connecting to MongoDB", err);
  });
