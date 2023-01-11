import React, { MouseEventHandler } from "react";
import styled from "styled-components";

export interface ItemContainerHomeProp {
  imgSrc: string;
  color: string;
  price: string;
  name: string;
  onClick?: MouseEventHandler<HTMLButtonElement>;
}

const ItemBoxBorder = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;

  position: relative;
  width: 27vw;
  min-width: 300px;
  height: 60vh;
  min-height: 400px;

  background: ${(props) => props.color || "#D6D6D6"};
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  border-radius: 30px;
`;

const TextContainer = styled.div`
  padding-top: 15%;
  padding-left: 10%;

  display: flex;
  flex-direction: column;

  width: 90%;
  height: 80px;
`;

const ItemBoxText = styled.div<{ isTitle: boolean }>`
  vertical-align: text-bottom;
  width: 100%;
  margin: 0;

  text-align: left;
  font-family: "Work Sans";
  font-weight: ${(props) => (props.isTitle ? 700 : 500)};
  font-size: ${(props) => (props.isTitle ? "xx-large" : "x-large")};

  color: #000000;
`;

const ItemContainerHome = ({
  imgSrc,
  color,
  price,
  name,
  onClick,
}: ItemContainerHomeProp) => {
  return (
    <>
      <ItemBoxBorder color={color}>
        <TextContainer>
          <ItemBoxText isTitle={true}>당신을 위한 {name}</ItemBoxText>
          <ItemBoxText isTitle={false}>{price}부터</ItemBoxText>
        </TextContainer>
        <img alt="item" src={imgSrc} width={"90%"}></img>
      </ItemBoxBorder>
    </>
  );
};
export default ItemContainerHome;
