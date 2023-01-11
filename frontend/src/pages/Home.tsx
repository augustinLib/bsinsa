import React, { useEffect, useState } from "react";
import styled from "styled-components";

import Header from "../components/Header";
import ItemContainerHome from "../components/ItemContainerHome";
import PageDesc from "../components/PageDesc";
import Navigation from "../components/Navigation/Navigation";
import axios from "axios";

const HomeContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 5%;

  padding-top: 8%;
  height: 65vh;
  background: #ebebeb;
  min-width: 1000px;
`;

const NavContainer = styled.div`
  height: 15vh;
  background: #ebebeb;
  min-width: 1000px;
`;

const Home = () => {
  const [data, setData] = useState([]);

  const searchApi = () => {
    axios.get("http://0.0.0.0:8000/data").then((response) => {
      setData(
        response.data
          .slice(1, -1)
          .split(",")
          .map((item: string) => parseInt(item))
      );
    });
  };

  useEffect(() => {
    searchApi();
  }, []);

  return (
    <div className="home">
      <Header />
      <PageDesc />
      <HomeContainer>
        {data.map((index, item) => (
          <ItemContainerHome
            key={index}
            imgSrc={`img/${index}.jpg`}
            color={"white"}
            price={"$9.99"}
            name={"신발 "}
          />
        ))}
        {/* <ItemContainerHome
          imgSrc={"img/shoes.png"}
          color={"white"}
          price={"$9.99"}
          name={"신발 "}
        />
        <ItemContainerHome
          imgSrc={"img/shoes.png"}
          color={"white"}
          price={"$9.99"}
          name={"신발 "}
        />
        <ItemContainerHome
          imgSrc={"img/shoes.png"}
          color={"white"}
          price={"$9.99"}
          name={"신발 "}
        /> */}
      </HomeContainer>
      <NavContainer>
        <Navigation />
      </NavContainer>
    </div>
  );
};

export default Home;
