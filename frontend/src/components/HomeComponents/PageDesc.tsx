import React from "react";
import styled from "styled-components";

const PageDescTextContainer = styled.div`
  position: absolute;
  width: 95vw;
  height: 60px;
  padding: 30px 0vw 0vh 5vw;
  margin: 0;
  background: #ebebeb;
  text-align: left;
  min-width: 950px;
`;

const PageDescText = styled.span<{ position: "first" | "second" }>`
  position: relative;
  height: 32px;

  font-family: "Work Sans";
  font-style: normal;
  font-weight: 600;
  font-size: 40px;
  margin-right: 20px;

  color: ${(props) =>
    props.position === "first" ? "#000000" : "rgba(0, 0, 0, 0.49)"};
`;

type PageDescProps = {
  category: string;
};
const PageDesc = ({ category }: PageDescProps) => {
  return (
    <>
      <PageDescTextContainer>
        <PageDescText position={"first"}>{category}</PageDescText>
        <PageDescText position={"second"}>
          당신만을 위한 최고의 추천
        </PageDescText>
      </PageDescTextContainer>
    </>
  );
};

export default PageDesc;
