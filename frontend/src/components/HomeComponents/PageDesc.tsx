import React from "react";
import styled from "styled-components";

export const PageDescTextContainer = styled.div`
  width: 100wh;
  min-width: 950px;
  height: 12vh;

  background: #ebebeb;
`;

const PageDescText = styled.div<{ position: "first" | "second" }>`
  display: flex;
  height: 100%;
  align-items: center;
  float: left;

  font-family: "Work Sans";
  font-style: normal;
  font-weight: 600;
  font-size: 40px;

  padding-left: ${(props) => (props.position === "first" ? "5%" : "2%")};
  color: ${(props) =>
    props.position === "first" ? "#000000" : "rgba(0, 0, 0, 0.49)"};
`;

type PageDescProps = {
  category: string;
};
const PageDesc = ({ category }: PageDescProps) => {
  return (
    <PageDescTextContainer>
      <PageDescText position={"first"}>{category}</PageDescText>
      <PageDescText position={"second"}>당신만을 위한 최고의 추천</PageDescText>
    </PageDescTextContainer>
  );
};

export default PageDesc;
