import axios from "axios";
import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Button from "../Buttons/Button";
import LogoButton from "../Buttons/Logo";

const Header = () => {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = React.useState(false);

  useEffect(() => {
    axios
      .get("api/check-login")
      .then((response) => {
        if (response.status === 200) {
          setIsLogin(response.data.isLoggedIn);
          console.log("login successful");
        } else {
          console.log("login failed");
        }
      })
      .catch((err) => {
        if (err.response.status === 401) {
          console.log(err);
          setIsLogin(false);
        }
      });
  }, [isLogin]);

  const handleLogout = () => {
    axios
      .get("api/logout")
      .then((response) => {
        if (response.status === 200) {
          setIsLogin(false);
          console.log("logout successful");
        } else {
          console.log("logout failed");
        }
        navigate("/");
      })
      .catch((err) => {
        console.log(err);
        navigate("/");
      });
  };

  return (
    <div className="Header">
      <div className="header-logo-box">
        <LogoButton />
      </div>
      <div className="header-button-box">
<<<<<<< HEAD
        <Button text="HOME" type="header" onClick={() => {}} />
        <Button
          text="EXPLORE"
          type="header"
          onClick={() => {
            navigate("/initial");
          }}
        />
=======
        <Button text="RECOMMENDATION" type="header" onClick={() => {}} />
        <Button text="EXPLORE" type="header" onClick={() => {navigate("/initial")}} />
>>>>>>> 159f3e53ab0569d98fff942a745fe2488732caf1
        {isLogin ? (
          <Button
            text="PROFILE"
            type="header"
            onClick={() => {
              navigate("/profile");
            }}
          />
        ) : (
          <Button
            text="PROFILE"
            type="header"
            onClick={() => {
              navigate("/login");
            }}
          />
        )}

        {isLogin ? (
          <Button text=" LOGOUT" type="header" onClick={handleLogout} />
        ) : (
          <Button
            text=" LOGIN"
            type="header"
            onClick={() => {
              navigate("/login");
            }}
          />
        )}
      </div>
    </div>
  );
};

export default Header;
