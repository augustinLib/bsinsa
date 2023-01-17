var express = require("express");
var path = require("path");
// var cookieParser = require('cookie-parser');
// var logger = require('morgan');

// var indexRouter = require('./routes/index');
// var usersRouter = require('./routes/users');

const cors = require("cors");
var app = express();

// app.use(logger('dev'));
// app.use(express.json());
// app.use(express.urlencoded({ extended: false }));
// app.use(cookieParser());
app.use(cors({ credentials: true, origin: "http://10.0.2.2:3000" }));
app.use(express.static(path.join(__dirname, "../frontend/build")));

app.get("*", function (req, res) {
  res.sendFile(path.join(__dirname, "../frontend/build", "index.html"));
});

app.listen(3000, () => {
  console.log("Server started on port 3000");
  console.log(path.join(__dirname, "../frontend/build/index.html"));
});

// app.use('/', indexRouter);
// app.use('/users', usersRouter);

// module.exports = app;
