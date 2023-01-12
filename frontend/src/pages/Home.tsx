import React, { useEffect, useState } from "react";
import styled from "styled-components";

import Header from "../components/Header";
import ItemContainerHome from "../components/ItemContainerHome";
import PageDesc from "../components/PageDesc";
import Navigation from "../components/Navigation/Navigation";
import axios from "axios";

export const HomeContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 5%;

  padding-top: 8%;
  height: 65vh;
  background: #ebebeb;
  min-width: 1000px;
`;

export const NavContainer = styled.div`
  height: 15vh;
  background: #ebebeb;
  min-width: 1000px;
`;

export interface ItemProp {
  product_num: number;
  category: string;
  price: string;
}

const Home = () => {
  const [data, setData] = useState<ItemProp[]>([]);

  const searchApi = () => {
    axios.get("http://0.0.0.0:8000/home-data").then((response) => {
      const pattern = /{(.*?)}/g;
      setData(
        response.data
          .slice(1, -1)
          .match(pattern)
          .map((item: string) => JSON.parse(item))
      );
    });
  };

  useEffect(() => {
    searchApi();
  }, []);

  return (
    <div className="home">
      <Header />
      <PageDesc category={"BSINSA"} />
      <HomeContainer>
        {data.map((item) => (
          <ItemContainerHome
            key={item.product_num}
            imgSrc={`img/${item.product_num}.jpg`}
            color={"white"}
            price={item.price}
            name={item.category}
          />
        ))}
      </HomeContainer>
      <NavContainer>
        <Navigation />
      </NavContainer>
    </div>
  );
};

export default Home;
