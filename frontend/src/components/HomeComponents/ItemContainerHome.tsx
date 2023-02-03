import React, { MouseEventHandler } from "react";
import styled from "styled-components";

const ItemBoxBorder = styled.div`
  float: left;

  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;

  position: static;
  width: 25vw;
  min-width: 300px;
  height: 60vh;
  min-height: 400px;

  background: ${(props) => props.color || "#D6D6D6"};
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  border-radius: 30px;
`;

export const TextContainer = styled.div`
  padding-top: 12%;
  padding-left: 10%;

  display: flex;
  flex-direction: column;
  text-align: left;

  width: 90%;
  height: 80px;
`;

export const ItemBoxText = styled.div<{ isTitle: boolean }>`
  vertical-align: text-bottom;
  width: 100%;
  height: 40px;

  white-space: nowrap;
  overflow: hidden;
  margin: 0;

  font-family: "Work Sans";
  font-weight: ${(props) => (props.isTitle ? 700 : 500)};
  font-size: ${(props) => (props.isTitle ? "xx-large" : "x-large")};

  color: #000000;
`;

const ImgContainer = styled.img`
  position: relative;
  max-width: 95%;
  max-height: 60%;
`;

export interface ItemContainerHomeProp {
  imgSrc: string;
  color: string;
  price: string;
  name: string;
  onClick: MouseEventHandler<HTMLDivElement>;
}

const ItemContainerHome = ({
  imgSrc,
  color,
  price,
  name,
  onClick,
}: ItemContainerHomeProp) => {
  return (
    <ItemBoxBorder color={color} onClick={onClick}>
      <TextContainer>
        <ItemBoxText isTitle={true}>당신을 위한 {name}</ItemBoxText>
        <ItemBoxText isTitle={false}>{price}부터</ItemBoxText>
      </TextContainer>
      <ImgContainer alt="item" src={imgSrc}></ImgContainer>
    </ItemBoxBorder>
  );
};
export default ItemContainerHome;
