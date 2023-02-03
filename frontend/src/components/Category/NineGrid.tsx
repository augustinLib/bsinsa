import styled, { css } from "styled-components";
import React from "react";

import { TextContainer } from "../HomeComponents/ItemContainerHome";
import { FourGridBorder, FourGridComponent, FourGridText } from "./FourGrid";
import {
  GridImgContainer,
  ItemProps,
  ArrayProps,
} from "./ItemContainerCategory";
import { useNavigate } from "react-router-dom";

const NineGridBorder = styled(FourGridBorder)`
  grid-template-columns: repeat(3, minmax(0, 1fr));
  grid-template-rows: repeat(3, minmax(0, 1fr));
`;

const NineGridComponentBig = styled(FourGridComponent)`
  grid-column: 1 / 2;
  grid-row: 1 / 2;
  grid-column: span 2;
  grid-row: span 2;

  display: grid;
  grid-template-columns: minmax(0, 1fr);
  grid-template-rows: minmax(0, 1fr) minmax(0, 3.3fr);
`;

const NineGridComponentSmall = styled(FourGridComponent)`
  border-radius: 12px;

  display: grid;
  grid-template-columns: minmax(0, 1fr);
  grid-template-rows: minmax(0, 1fr) minmax(0, 4fr);
`;

const NineGridTextContainer = styled(TextContainer)<{ isBig: boolean }>`
  padding-top: 0;

  display: flex;
  justify-content: flex-end;
  flex-direction: column;

  height: 100%;
  ${(props) =>
    props.isBig
      ? css`
          width: 80%;
          text-align: left;
          padding-left: 5%;
        `
      : css`
          width: 100%;
          text-align: center;
          padding-left: 0%;
        `}
  height: 100%;
`;

const NineGridText = styled(FourGridText)<{ isBig: boolean; isTitle: boolean }>`
  ${(props) =>
    props.isBig
      ? css`
          font-size: ${props.isTitle ? "x-large" : "large"};
          font-weight: ${props.isTitle ? 700 : 500};
          text-align: left;
        `
      : css`
          font-size: "xx-large";
          font-weight: 800;
          text-align: center;
          margin-top: auto;
        `};
  font-family: "Work Sans";

  color: #000000;
`;

export const GridImg = styled.img`
  margin-top: 1%;
  position: relative;
  padding-top: 5%;
  max-width: 80%;
  max-height: 70%;
`;

const ItemOfNineBig = ({ product_num, product_name, price }: ItemProps) => {
  const publicUrl = process.env.PUBLIC_URL;
  const navigate = useNavigate();
  return (
    <NineGridComponentBig
      onClick={(): void => navigate(`/item/${product_num}`)}>
      <NineGridTextContainer isBig={true}>
        <NineGridText isBig={true} isTitle={true}>
          {product_name}
        </NineGridText>
        <NineGridText isBig={true} isTitle={false}>
          {price}
        </NineGridText>
      </NineGridTextContainer>
      <GridImgContainer>
        <GridImg src={`${publicUrl}/img/${product_num}.jpg`} />
      </GridImgContainer>
    </NineGridComponentBig>
  );
};

const ItemOfNineSmall = ({ product_num, product_name, price }: ItemProps) => {
  const publicUrl = process.env.PUBLIC_URL;
  const navigate = useNavigate();
  return (
    <NineGridComponentSmall
      onClick={(): void => navigate(`/item/${product_num}`)}>
      <NineGridTextContainer isBig={false}>
        <NineGridText isBig={false} isTitle={false}>
          {price}
        </NineGridText>
      </NineGridTextContainer>
      <GridImgContainer>
        <GridImg src={`${publicUrl}/img/${product_num}.jpg`} />
      </GridImgContainer>
    </NineGridComponentSmall>
  );
};

const NineGridContainer: React.FC<ArrayProps> = ({ propWhichIsArray }) => {
  return (
    <NineGridBorder>
      {propWhichIsArray.slice(0, 1).map((item) => (
        <ItemOfNineBig
          key={item.product_num}
          product_num={item.product_num}
          product_name={item.product_name}
          price={item.price}
        />
      ))}
      {propWhichIsArray.slice(1).map((item) => (
        <ItemOfNineSmall
          key={item.product_num}
          product_num={item.product_num}
          price={item.price}
          product_name={item.product_name}
        />
      ))}
    </NineGridBorder>
  );
};

export default NineGridContainer;
