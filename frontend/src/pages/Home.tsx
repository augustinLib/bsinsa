import React from "react";
import styled from "styled-components";

import Header from "../components/Header";
import ItemContainerHome from "../components/ItemContainerHome";
import PageDesc from "../components/PageDesc";

const HomeContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 5%;

  padding-top: 12%;
  height: 75vh;
  background: #ebebeb;
`;

const Home = () => {
  return (
    <div className="home">
      <Header />
      <PageDesc />
      <HomeContainer>
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
        />
        <ItemContainerHome
          imgSrc={"img/shoes.png"}
          color={"white"}
          price={"$9.99"}
          name={"신발 "}
        />
      </HomeContainer>
    </div>
  );
};

export default Home;
