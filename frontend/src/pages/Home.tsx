import React from "react";
import styled from "styled-components";

import Header from "../components/Header";
import ItemContainerHome from "../components/ItemContainerHome";
import PageDesc from "../components/PageDesc";
import Navigation from "../components/Navigation/Navigation";

const HomeContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 5%;

  padding-top: 12%;
  height: 60vh;
  background: #ebebeb;
  min-width: 1000px;
`;

const NavContainer = styled.div`
  height: 15vh;
  background: #ebebeb;
  min-width: 1000px;
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
      <NavContainer>
        <Navigation />
      </NavContainer>
    </div>
  );
};

export default Home;
