import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { useState, useEffect, createContext } from "react";

import Home from "./pages/Home";
import TryOn from "./pages/TryOn";
import Profile from "./pages/Profile";
import ItemList from "./pages/ItemList";
import Item from "./pages/Item";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Initialization from "./pages/Initialization";

function App() {
  const [user, setUser] = useState(sessionStorage.getItem("token"));
  const UserLogin = createContext();

  useEffect(() => {
    const token = sessionStorage.getItem("token");
    if (token) {
      setUser(true);
    }
  }, []);

  return (
    <UserLogin.Provider value={user}>
      <BrowserRouter>
        <div className="App">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/tryon" element={<TryOn />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/category/:id" element={<ItemList />} />
            <Route path="/item/:id" element={<Item />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/initial" element={<Initialization />} />
          </Routes>
        </div>
      </BrowserRouter>
    </UserLogin.Provider>
  );
}

export default App;
