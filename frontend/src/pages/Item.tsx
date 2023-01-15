import React, { useEffect, useState } from "react";
import styled from "styled-components";

import Header from "../components/HomeComponents/Header";
import Navigation from "../components/Navigation/Navigation";
import { HomeContainer, NavContainer } from "./Home";
import { useNavigate, useParams } from "react-router-dom";
import {
  TextContainer,
  ItemBoxText,
} from "../components/HomeComponents/ItemContainerHome";
import axios from "axios";

export const ItemContainer = styled(HomeContainer)`
  display: flex;
  flex-direction: row;
  justify-content: center;

  padding-top: 8%;
  height: 65vh;
  background: #ebebeb;
  min-width: 1000px;
`;

const ItemImageContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  vertical-align: middle;
  overflow: hidden;

  width: 35vw;
  height: 60vh;
  min-width: 300px;
  min-height: 400px;

  background: white;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  border-radius: 30px;
`;
const ItemImg = styled.img`
  object-fit: scale-down;

  width: 90%;
  height: 90%;
`;
const RightContatiner = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0px 20px;
  height: 60vh;
`;

const ItemDescContainer = styled.div`
  grid-column: 1/3;
  grid-row: 1/2;
  display: box;
  align-items: center;
  justify-content: center;

  width: 45vw;
  min-width: 300px;
  height: 45vh;
  min-height: 300px;

  background: white;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  border-radius: 30px;
`;

const ItemTextContainer = styled(TextContainer)`
  padding-top: 2%;
  padding-left: 5%;

  display: flex;

  width: 90%;
  height: 20%;
`;

const ItemDescText = styled(ItemBoxText)`
  box-sizing: border-box;
`;

const ReviewContainer = styled.div`
  display: flex;
  width: 96%;
  height: 70%;
  margin: 2%;
  background: #f8f8f8;

  justify-content: center;
`;

const Button = styled.button<{ color: string }>`
  ${(props) => (props.color ? `background: ${props.color}` : "#1c1f33")};
  color: white;
  border: none;
  border-radius: 5px;

  font-weight: 700;
  font-style: bold;
  font-size: 150%;
  font-family: "Work Sans";

  text-align: center;
  text-transform: capitalize;

  &:hover {
    font-weight: 900;
    font-style: italic;
  }
`;

export interface ItemProp {
  product_num: number;
  product_name: string;
  price: string;
}

const Item = () => {
  const { id = "100138" } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState<ItemProp>({
    product_name: "",
    price: "",
    product_num: 0,
  });

  const searchItem = () => {
    axios.get(`http://0.0.0.0:8000/item/${id}`).then((response) => {
      const pattern = /{(.*?)}/g;
      setData(
        response.data
          .slice(1, -1)
          .match(pattern)
          .map((item: string) => JSON.parse(item))[0]
      );
    });
  };

  useEffect(() => {
    searchItem();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="home">
      <Header />
      <HomeContainer>
        <ItemImageContainer>
          <ItemImg src={`/img/${id}.jpg`} />
        </ItemImageContainer>
        <RightContatiner>
          <ItemDescContainer>
            <ItemTextContainer>
              <ItemDescText isTitle={true}>{data.product_name}</ItemDescText>
              <ItemDescText isTitle={false}>{data.price}</ItemDescText>
            </ItemTextContainer>
            <ReviewContainer>asdffdasdfasdfasdfdfassdfas</ReviewContainer>
          </ItemDescContainer>
          <Button
            color={"#1c1f33"}
            onClick={() => {
              navigate("/");
            }}>
            구매하기
          </Button>
          <Button
            color={"#2E4D64"}
            onClick={() => {
              navigate("/");
            }}>
            장바구니
          </Button>
        </RightContatiner>
      </HomeContainer>
      <NavContainer>
        <Navigation />
      </NavContainer>
    </div>
  );
};

export default Item;
