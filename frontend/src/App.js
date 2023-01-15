import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import Home from "./pages/Home";
import TryOn from "./pages/TryOn";
import Profile from "./pages/Profile";
import ItemList from "./pages/ItemList";
import Item from "./pages/Item";

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/tryon" element={<TryOn />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/category/:id" element={<ItemList />} />
          <Route path="/item/:id" element={<Item />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
