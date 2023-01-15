import styled from "styled-components";
import React from "react";
import { TextContainer } from "../HomeComponents/ItemContainerHome";
import { useNavigate } from "react-router-dom";

export const FourGridBorder = styled.div`
  width: 25vw;
  min-width: 300px;
  height: 60vh;
  min-height: 400px;

  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 20px;

  background-color: #ebebeb;
  padding: 1px;
`;

export const FourGridComponent = styled.div`
  padding: 0px;
  border-radius: 20px;

  width: 100%;
  height: auto;
  background-color: #ffffff;

  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
`;

export const FourGridTextContainer = styled(TextContainer)`
  padding-top: 5%;
  padding-left: 5%;

  display: flex;
  flex-direction: column;

  width: 90%;
  height: 15%;
`;

export const FourGridText = styled.div<{ isTitle: boolean }>`
  vertical-align: text-bottom;
  width: 100%;
  margin: 0;

  display: inline;
  text-align: left;
  font-family: "Work Sans";
  font-size: ${(props) => (props.isTitle ? "small" : "small")};
  font-weight: ${(props) => (props.isTitle ? 700 : 500)};
  color: #000000;
`;

export const GridImg = styled.img`
  position: relative;
  padding-top: 5%;
  max-width: 80%;
  max-height: 80%;
`;

export interface ItemProps {
  product_num: number;
  product_name: string;
  price: string;
}

export interface ArrayProps {
  propWhichIsArray: ItemProps[];
}

const ItemOfFour = ({ product_num, product_name, price }: ItemProps) => {
  const publicUrl = process.env.PUBLIC_URL;
  const navigate = useNavigate();
  return (
    <FourGridComponent onClick={(): void => navigate(`/item/${product_num}`)}>
      <FourGridTextContainer>
        <FourGridText isTitle={true}>{product_name}</FourGridText>
        <FourGridText isTitle={false}>{price}</FourGridText>
      </FourGridTextContainer>
      <GridImg src={`${publicUrl}/img/${product_num}.jpg`} />
    </FourGridComponent>
  );
};
// const Component: React.FC<Props> = ({ propWhichIsArray })
const FourGridContainer: React.FC<ArrayProps> = ({ propWhichIsArray }) => {
  return (
    <FourGridBorder>
      {propWhichIsArray.map((item) => (
        <ItemOfFour
          key={item.product_num}
          product_num={item.product_num}
          price={item.price}
          product_name={item.product_name}
        />
      ))}
    </FourGridBorder>
  );
};

export default FourGridContainer;
