import React from "react";
import { useNavigate } from "react-router-dom";

const LogoButton = () => {
  const publicUrl = process.env.PUBLIC_URL;
  const navigate = useNavigate();
  return (
    <button className="logo">
      <div onClick={(): void => navigate(`/`)}>
        <img
          className="logo-image"
          alt="logo"
          src={`${publicUrl}/img/logo.png`}
        />
      </div>
    </button>
  );
};

export default LogoButton;
