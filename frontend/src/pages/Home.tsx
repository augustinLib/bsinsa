import React, { useEffect, useState } from "react";
import styled from "styled-components";

import Header from "../components/HomeComponents/Header";
import ItemContainerHome from "../components/HomeComponents/ItemContainerHome";
import PageDesc from "../components/HomeComponents/PageDesc";
import Navigation from "../components/Navigation/Navigation";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export const HomeContainer = styled.div`
  display: flex;
  flex: 1;

  justify-content: space-around;
  padding-left: 5%;
  padding-right: 5%;

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
  onClick: (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => void;
}

const Home = () => {
  const [data, setData] = useState<ItemProp[]>([]);
  const navigate = useNavigate();

  const searchApi = (ip?: string) => {
    axios
      .get("api/data")
      .then((response) => {
        const pattern = /{(.*?)}/g;
        setData(
          response.data
            .slice(1, -1)
            .match(pattern)
            .map((item: string) => JSON.parse(item))
        );
      })
      .catch((error) => {
        console.log(error);
      });

    // axios.get("http://127.0.0.1:8000/home-data").then((response) => {
    //   const pattern = /{(.*?)}/g;
    //   setData(
    //     response.data
    //       .slice(1, -1)
    //       .match(pattern)
    //       .map((item: string) => JSON.parse(item))
    //   );
    // });
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
            onClick={(): void => navigate(`/item/${item.product_num}`)}
          />
        ))}
      </HomeContainer>
      <NavContainer>
        <Navigation />
        {/* <Dialog /> */}
      </NavContainer>
    </div>
  );
};

export default Home;
