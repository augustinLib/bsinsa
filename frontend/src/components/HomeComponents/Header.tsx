import axios from "axios";
import React, { useEffect, memo } from "react";
import { useNavigate } from "react-router-dom";
import Button from "../Buttons/Button";
import LogoButton from "../Buttons/Logo";

const Header = () => {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = React.useState(false);

  useEffect(() => {
    if (isLogin) {
      setIsLogin(true);
    } else {
    axios
      .get("/api/check-login")
      // .get("/api/user")
      .then((response) => {
        if (response.status === 200) {
          setIsLogin(response.data.isLoggedIn);
          console.log("login checked");
        } else {
          console.log("login checking failed");
        }
      })
      .catch((err) => {
        if (err.response.status === 401) {
          console.log(err);
          setIsLogin(false);
        }
      });
    }
  }, []);

  const handleLogout = () => {
    axios
      .get("/api/logout")
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
        <Button text="HOME" type="header" onClick={() => {}} />
        <Button
          text="EXPLORE"
          type="header"
          onClick={() => {
            navigate("/initial");
          }}
        />
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

export default memo(Header);
