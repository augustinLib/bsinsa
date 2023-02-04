import React, { useEffect, useReducer, useState } from "react";
import styled from "styled-components";

import Header from "../components/HomeComponents/Header";
import Navigation from "../components/Navigation/Navigation";
import { NavContainer } from "./Home";
import { PageDescTextContainer } from "../components/HomeComponents/PageDesc";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import { emptyProps, ItemProps, propMatcher } from "../etc/propMatcher";

const HomeContainer = styled.div`
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.5fr);
  grid-template-rows: 1fr;
  background: #ebebeb;
  min-width: 1000px;
  gap: 5%;

  height: 67vh;

  padding-left: 5%;
  padding-right: 5%;
  padding-bottom: 2%;

  background: #ebebeb;
  min-width: 1000px;
`;

export const ItemContainer = styled.div`
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.5fr);
  grid-template-rows: 1fr;
  background: #ebebeb;
  min-width: 1000px;
  // justify-content: center;

  height: 65vh;
`;

const ItemImageContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  vertical-align: middle;
  overflow: hidden;

  // width: 35vw;
  // height: 60vh;
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

const RightContainer = styled.div`
  display: grid;
  width: 95%;
  grid-template-columns: minmax(0, 1fr);
  grid-template-rows: minmax(0, 1fr) minmax(0, 2.5fr);
  row-gap: 5%;
`;

const ItemDescContainer = styled.div`
  grid-column: 1/3;
  grid-row: 1/2;

  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) minmax(0, 1fr) minmax(
      0,
      1fr
    );
  grid-template-rows: minmax(0, 1fr) minmax(0, 1fr);
  padding-left: 8%;
  padding-right: 5%;
  padding-bottom: 2%;

  background: white;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  border-radius: 30px;
`;

const ItemTextContainer = styled.div`
  grid-column: 1/5;

  width: 95%;
  vertical-align: bottom;
  align-self: end;
`;

const ItemDescText = styled.div<{ isTitle: boolean }>`
  vertical-align: ${(props) => (props.isTitle ? "top" : "sub")};

  white-space: nowrap;
  overflow: hidden;
  margin: 0;

  text-align: left;
  align-self: center;
  font-family: "Work Sans";
  font-weight: ${(props) => (props.isTitle ? 700 : 400)};
  font-size: ${(props) => (props.isTitle ? "xx-large" : "xx-large")};

  color: #000000;
  box-sizing: border-box;
`;

const Button = styled.button<{ loc: "left" | "center" | "right" }>`
  background: ${(props) =>
    props.loc === "left"
      ? "#000000"
      : props.loc === "center"
      ? "#ebebeb"
      : "#ff5c5c"};
  color: ${(props) =>
    props.loc === "left"
      ? "white"
      : props.loc === "center"
      ? "black"
      : "white"};
  border: none;
  border-radius: 5px;
  width: 90%;
  height: 70%;
  align-self: center;
  justify-self: left;

  font-weight: 700;
  font-style: bold;
  font-size: 150%;
  font-family: "Work Sans";

  text-align: center;
  text-transform: capitalize;

  &:hover {
    font-weight: 900;
    font-style: italic;
    cursor: pointer;
  }

  &:active {
    margin-left: 5px;
    margin-top: 5px;
  }
`;

const DetailsContainer = styled.div`
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  grid-template-rows: minmax(0, 1fr);
  width: 100%;
  padding: 0;
  gap: 5%;
`;

const Detail = styled.div`
  display: flex;
  background: white;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  border-radius: 30px;
  border: none;

  width: 100%;

  font-size: x-large;
  font-weight: 900;
  text-align: center;
  vertical-align: middle;
  justify-content: center;
  align-items: center;

  white-space: pre-wrap;
`;

export interface ItemProp {
  product_num: number;
  product_name: string;
  price: string;
  category?: string;
}

interface TagLabelProp {
  tag: string[];
  label: string
}

const Item = () => {
  const { id = "100138" } = useParams();
  const navigate = useNavigate();
  const [liked, setLiked] = React.useState<ItemProps>(emptyProps);
  const [likeClicked, setLikeClicked] = React.useState(false);  
  const [userId, setUserId] = React.useState("");
  const [data, setData] = useState<ItemProp>({
    product_name: "",
    price: "",
    product_num: 0,
  });

  const [tagLabel, setTagLabel] = useState<TagLabelProp>({
    tag: [],
    label: ""
  })

  const getKeyByValue = (obj: any, value: any) => {
    return Object.keys(obj).find((key) => obj[key] === value);
  };

  const getUser = () => {
    axios
      .get("/api/user")
      .then((response) => {
        setUserId(response.data.user.userId);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  // saved!
  const handleLike = () => {
    if (!likeClicked) {
      const category = data.category;
      const categoryEng = getKeyByValue(propMatcher, category);
      const product_num = data.product_num;
      const temp = { ...liked };
      temp[categoryEng as keyof ItemProps].push(product_num);
      setLiked(temp);
      setLikeClicked(true);
    } 
  };

  const searchItem = () => {
    axios.get(`/api/item-data/${id}`).then((response) => {
      // axios.get(`http://0.0.0.0:8001/item/${id}`).then((response) => {
      const pattern = /{(.*?)}/g;
      setData(
        response.data
          .slice(1, -1)
          .match(pattern)
          .map((item: string) => JSON.parse(item))[0]
      );
    });
  };

  const getTagLabel = () => {
    axios.get(`/api/tag-label/${id}`).then((response) => {
      setTagLabel(
        response.data
      );
    });
  }

  useEffect(() => {
    searchItem();
    getUser();
    getTagLabel();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    axios
      .post("/api/likes", {
        userId: userId,
        liked: liked,
      })
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [liked, userId]);

  return (
    <div className="home">
      <Header />
      <PageDescTextContainer />
      <HomeContainer>
        <ItemImageContainer>
          <ItemImg src={`/img/${id}.jpg`} />
        </ItemImageContainer>
        <RightContainer>
          <ItemDescContainer>
            <ItemTextContainer>
              <ItemDescText isTitle={true}>{data.product_name}</ItemDescText>
            </ItemTextContainer>
            <ItemDescText isTitle={false}>{data.price}</ItemDescText>
            <Button
              loc="left"
              onClick={() => {
                navigate("/");
              }}>
              구매하기
            </Button>
            <Button
              loc="center"
              onClick={() => {
                navigate("/");
              }}>
              장바구니
            </Button>
            <Button loc="right" onClick={handleLike}>
              좋아요
            </Button>
          </ItemDescContainer>
          <DetailsContainer>
            <Detail>
              {tagLabel.tag.length !== 0 ? tagLabel.tag.map((item) => item + `\n`) : "로딩 중입니다"}
            </Detail>
            <Detail>
              {tagLabel.label !== "" ? tagLabel.label : "로딩 중입니다"}
            </Detail>
          </DetailsContainer>
        </RightContainer>
      </HomeContainer>
      <NavContainer>
        <Navigation />
      </NavContainer>
    </div>
  );
};

export default Item;
