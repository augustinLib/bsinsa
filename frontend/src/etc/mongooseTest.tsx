// create a mongoose test file
import mongoose, { Mongoose } from "mongoose";

const MONGODB_URI = "localhost:27017";

const connectToMongoDb = async (): Promise<Mongoose> => {
  try {
    await mongoose.connect(MONGODB_URI, {});
    console.log("MongoDB connected...");
    return mongoose;
  } catch (err) {
    console.log(err);
    throw new Error("Error connecting to MongoDB");
  }
};

export default connectToMongoDb;
