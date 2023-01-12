import React from "react";
import styled from "styled-components";
import { GridImg } from "./FourGrid";
import { ItemProps } from "./FourGrid";
import { useNavigate } from "react-router-dom";

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
  padding-top: 5%;
  padding-left: 5%;

  display: inline-block;
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

const OneGridImg = styled(GridImg)`
  width: 80%;
  max-height: 70%;
  max-width: 80%;
  padding-top: 0px;
`;

// TODO : fix it using Array Structure
const OneGrid = ({ product_num, product_name, price }: ItemProps) => {
  const publicUrl = process.env.PUBLIC_URL;
  const navigate = useNavigate();
  return (
    <>
      <ItemBoxBorder
        color={"white"}
        onClick={(): void => navigate(`/item/${product_num}`)}>
        <TextContainer>
          <ItemBoxText isTitle={true}>{product_name}</ItemBoxText>
          <ItemBoxText isTitle={false}>{price}</ItemBoxText>
        </TextContainer>
        <OneGridImg alt="item" src={`${publicUrl}/img/${product_num}.jpg`} />
      </ItemBoxBorder>
    </>
  );
};
export default OneGrid;
