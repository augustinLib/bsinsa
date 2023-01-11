import React, { MouseEventHandler } from "react";

export interface ButtonProp {
  text: string;
  type: "header" | "navigation";
  onClick?: MouseEventHandler<HTMLButtonElement>;
}

const Button = ({ text, type, onClick }: ButtonProp) => {
  return (
    <button className={`Button_${type}`} onClick={onClick}>
      <p className="button-text">{text}</p>
    </button>
  );
};

export default Button;
