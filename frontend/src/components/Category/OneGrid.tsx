import React from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";

import {
  ItemProps,
  ArrayProps,
  GridImg,
  GridImgContainer,
} from "./ItemContainerCategory";

const OneItemBoxBorder = styled.div`
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  grid-template-rows: minmax(0, 1fr) minmax(0, 4.5fr);
  overflow: hidden;

  width: 27vw;
  min-width: 300px;
  height: 60vh;
  min-height: 400px;

  background: ${(props) => props.color || "#D6D6D6"};
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  border-radius: 30px;
`;

const OneItemTextContainer = styled.div`
  padding-left: 10%;

  display: flex;
  justify-content: flex-end;
  flex-direction: column;

  width: 80%;
  height: 100%;
`;

const OneItemBoxText = styled.div<{ isTitle: boolean }>`
  vertical-align: text-bottom;
  width: 100%;
  margin: 0;

  white-space: nowrap;
  overflow-x: auto;
  text-overflow: ellipsis;

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
const ItemOfOne = ({ product_num, product_name, price }: ItemProps) => {
  const publicUrl = process.env.PUBLIC_URL;
  const navigate = useNavigate();
  return (
    <OneItemBoxBorder
      color={"white"}
      onClick={(): void => navigate(`/item/${product_num}`)}>
      <OneItemTextContainer>
        <OneItemBoxText isTitle={true}>{product_name}</OneItemBoxText>
        <OneItemBoxText isTitle={false}>{price}</OneItemBoxText>
      </OneItemTextContainer>
      <GridImgContainer>
        <OneGridImg alt="item" src={`${publicUrl}/img/${product_num}.jpg`} />
      </GridImgContainer>
    </OneItemBoxBorder>
  );
};

const OneGrid: React.FC<ArrayProps> = ({ propWhichIsArray }) => {
  return (
    <>
      {propWhichIsArray.map((item) => (
        <ItemOfOne
          product_num={item.product_num}
          product_name={item.product_name}
          price={item.price}
        />
      ))}
    </>
  );
};
export default OneGrid;
