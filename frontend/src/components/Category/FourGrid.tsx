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
  grid-template-columns: repeat(2, minmax(0, 1fr));
  grid-template-rows: repeat(2, minmax(0, 1fr));

  gap: 20px;
  background-color: #ebebeb;
`;

export const FourGridComponent = styled.div`
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  grid-template-rows: minmax(0, 1fr) minmax(0, 3fr);
  border-radius: 20px;
  overflow: hidden;

  width: 100%;
  height: 100%;
  background-color: #ffffff;

  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
`;

export const FourGridTextContainer = styled(TextContainer)`
  padding-top: 0;
  padding-left: 0;
  text-align: left;
  justify-content: bottom;

  width: 100%;
  height: 100%;
`;

export const FourGridText = styled.div<{ isTitle: boolean }>`
  width: 100%;
  height: fit-content;

  white-space: nowrap;
  overflow-x: auto;
  text-overflow: ellipsis;

  font-family: "Work Sans";
  font-size: ${(props) => (props.isTitle ? "x-large" : "large")};
  font-weight: ${(props) => (props.isTitle ? 700 : 500)};
  color: #000000;
`;

export const GridImgContainer = styled.div`
  display: flex;
  overflow: hidden;
  justify-content: center;
  align-items: center;
`;

export const GridImg = styled.img`
  width: 80%;
  max-height: 80%;
  object-fit: cover;
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
      <GridImgContainer>
        <GridImg src={`${publicUrl}/img/${product_num}.jpg`} />
      </GridImgContainer>
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
