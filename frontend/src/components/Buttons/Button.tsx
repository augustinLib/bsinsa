import React, { MouseEventHandler } from "react";
import styled from "styled-components";

export interface ButtonProp {
  text: string;
  type: "header" | "navigation";
  onClick?: MouseEventHandler<HTMLButtonElement>;
}
export const HeaderButton = styled.button<{ typeOf: "header" | "navigation" }>`
  margin-left: 10px;
  margin-right: 10px;
  padding: ${(props) =>
    props.typeOf === "header" ? "0px" : "20px 20px 15px 15px"};
  position: relative;
  width: ${(props) => (props.typeOf === "header" ? "fit-content" : "auto")};
  height: 100%;

  background: ${(props) => (props.typeOf === "header" ? "000000" : "#1c1f33")};
  color: #ffffff;
  border: ${(props) => (props.typeOf === "header" ? "black" : "none")};
  border-radius: 5px;

  font-weight: 700;
  font-style: bold;
  font-size: 20px;
  font-family: "Work Sans";

  vertical-align: middle;
  text-align: center;
  text-transform: capitalize;

  &:hover {
    color: #ee0260;
    font-weight: 900;
  }
`;

const Button = ({ text, type, onClick }: ButtonProp) => {
  return (
    <HeaderButton onClick={onClick} typeOf={type}>
      {text}
    </HeaderButton>
  );
};

export default Button;
