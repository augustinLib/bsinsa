import React from "react";
import { useNavigate } from "react-router-dom";
import Button from "../Buttons/Button";
import LogoButton from "../Buttons/Logo";

const Header = () => {
  const navigate = useNavigate();

  return (
    <div className="Header">
      <div className="header-logo-box">
        <LogoButton />
      </div>
      <div className="header-button-box">
        <Button text="RECOMMENDATION" type="header" onClick={() => {}} />
        <Button text="EXPLORE" type="header" onClick={() => {}} />
        <Button
          text="PROFILE"
          type="header"
          onClick={() => {
            navigate("/profile");
          }}
        />
        <Button text=" LOGOUT" type="header" onClick={() => {}} />
      </div>
    </div>
  );
};

export default Header;
