import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "../Buttons/Button";
import styled, { css } from "styled-components";

const NavigationContainer = styled.div<{ category: "top" | "bottom" }>``;
const NavSection = styled.div<{ isOn: boolean }>`
  
  position: relative;
  flex-direction: row;
  float: right;
  background-color: #1c1f33;
  border: 0px;
  border-radius: 5px;
  margin-right: 10px;

  bottom: 0;
  transition: transform 0.5s ease-in-out, visibility 0.5s ease-in-out;
  visibility: ${(props) => (props.isOn ? "0.5s ease-in-out" : "hidden")};
  ${(props) =>
    props.isOn &&
    css`
      transform: translateX(0%);
    `}
  ${(props) =>
    !props.isOn &&
    css`
      transform: translateX(100%);
    `}
  }
`;

const Navigation = () => {
  const [isOn, setIsOn] = useState(false);
  const [category, setCategory] = useState<"top" | "bottom">("top");
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

  useEffect(() => {
    if (!isOn) {
      setTimeout(() => {
        setIsOn(false);
      }, 500);
    }
  }, [isOn]);

  return (
    <NavigationContainer category={category}>
      <NavSection isOn={true}>
        {isOn ? (
          <Button
            text="HIDE"
            type="navigation"
            onClick={() => {
              setIsOn(!isOn);
            }}
          />
        ) : null}
      </NavSection>
      <NavSection isOn={true}>
        <Button
          text="TOP"
          type="navigation"
          onClick={() => {
            !isOn && setIsOn(!isOn);
            setCategory("top");
          }}
        />
        <Button
          text="BOTTOM"
          type="navigation"
          onClick={() => {
            !isOn && setIsOn(!isOn);
            setCategory("bottom");
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
                    setIsOn(false);
                    navigate(`/category/${item.toLowerCase()}`);
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
                    setIsOn(false);
                    navigate(`/category/${item.toLowerCase()}`);
                  }}
                />
              );
            })}
      </NavSection>
    </NavigationContainer>
  );
};

export default Navigation;
