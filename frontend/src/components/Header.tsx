import React from "react";
import Button from "./Buttons/Button";
import LogoButton from "./Buttons/Logo";

const Header = () => {
  return (
    <div className="Header">
      <div className="header-button-box">
        <Button text="TRYON" type="header" onClick={() => {}} />
        <Button text="RECOMMENDATION" type="header" onClick={() => {}} />
        <Button text="BUSINESS" type="header" onClick={() => {}} />
        <Button text="PROFILE" type="header" onClick={() => {}} />
      </div>
      <div className="header-logo-box">
        <LogoButton />
      </div>
    </div>
  );
};

export default Header;
