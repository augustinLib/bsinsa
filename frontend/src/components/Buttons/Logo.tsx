import React from "react";

const LogoButton = () => {
  const publicUrl = process.env.PUBLIC_URL;

  return (
    <button className="logo">
      <div>
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
