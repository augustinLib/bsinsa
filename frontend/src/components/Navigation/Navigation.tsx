import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "../Buttons/Button";
import styled from "styled-components";

const NavigationContainer = styled.div<{ category: "top" | "bottom" }>``;
const NavSection = styled.div<{ isOn: boolean }>`
  display: ${(props) => (props.isOn ? "block" : "none")};
  position: relative;
  flex-direction: row;
  float: right;
  background-color: #1c1f33;
  border: 0px;
  border-radius: 5px;
  margin-right: 10px;

  .appear {
    animation: appear 1s ease-in-out;
  }
`;

const Navigation = () => {
  const [isOn, setIsOn] = useState(false);
  const [category, setCategory] = useState<"top" | "bottom">("top");
  const [toggle, setToggle] = useState(false);
  const navigate = useNavigate();
  const topArray = [
    "HOOD",
    "KNIT",
    "LONG",
    "POLO",
    "SHIRT",
    "SHORT",
    "SLEEVELESS",
    "SWEAT",
  ];
  const bottomArray = [
    "COTTON",
    "DENIM",
    "JOGGER",
    "JUMPER",
    "LEGGINGS",
    "SHORT",
    "SLACKS",
    "ETC",
  ];

  return (
    <NavigationContainer category={category}>
      <NavSection isOn={true}>
        <Button
          text="TOP"
          type="navigation"
          onClick={() => {
            !isOn && setIsOn(!isOn);
            setCategory("top");
            setToggle(true);
          }}
        />
        <Button
          text="BOTTOM"
          type="navigation"
          onClick={() => {
            !isOn && setIsOn(!isOn);
            setCategory("bottom");
            setToggle(true);
          }}
        />
        <Button
          text={toggle ? "HIDE" : "SHOW"}
          type="navigation"
          onClick={() => {
            setIsOn(!isOn);
            setToggle(!toggle);
          }}
        />
      </NavSection>
      <NavSection isOn={isOn}>
        {category === "top"
          ? topArray.map((item, index) => {
              return (
                <Button
                  key={index}
                  text={item}
                  type="navigation"
                  onClick={() => {
                    navigate(`/category/${item.toLowerCase()}`);
                    setToggle(false);
                  }}
                />
              );
            })
          : bottomArray.map((item, index) => {
              return (
                <Button
                  key={index}
                  text={item}
                  type="navigation"
                  onClick={() => {
                    navigate(`/category/${item.toLowerCase()}`);
                    setToggle(false);
                  }}
                />
              );
            })}
      </NavSection>
    </NavigationContainer>
  );
};

export default Navigation;
