import React from "react";
import styled from "styled-components";

const LoginBox = () => {
  return (
    <div className="LoginBox">
      <div className="login-box">
        <div className="login-box-header">Login</div>
        <div className="login-box-body">
          <div className="login-box-body-input">
            <input type="text" placeholder="Username" />
          </div>
          <div className="login-box-body-input">
            <input type="password" placeholder="Password" />
          </div>
          <div className="login-box-body-button">
            <button>LOGIN</button>
            <span className="material-symbols-outlined">settings</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginBox;
