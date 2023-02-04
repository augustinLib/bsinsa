import React, { useEffect, useState } from "react";
import LoginHeader from "../components/Login/LoginHeader";
import styled, { keyframes } from "styled-components";
import axios from "axios";
import {
  ItemProps,
  propMatcher,
  propMatcherProps,
  emptyProps,
} from "../etc/propMatcher";
import { useNavigate } from "react-router-dom";

const fadeIn = keyframes`
  from { opacity: 0;}
  to { opacity: 1;}
`;

const fadeOut = keyframes`
  from { opacity: 1; }
  to { opacity: 0; }
`;

const BackGround = styled.div`
  display: flex;
  flex-direction: column;
  flex: 1;
  gap: 5%;
  justify-content: center;
  align-items: center;
  background: #ebebeb;
  min-width: 1000px;
`;

const InitHome = styled.div<{ nextClicked: boolean }>`
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  width: 95%;
  height: 80%;
  gap: 2%;
  border-radius: 30px;
  transition: 0.5s ease-in-out;
  animation: ${(props) => (props.nextClicked ? fadeOut : fadeIn)} 1s ease-in;
`;

const ItemContainer = styled.div`
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  grid-template-rows:
    minmax(0, 0.3fr) minmax(0, 1fr)
    minmax(0, 1fr) minmax(0, 1fr);
  background: #ebebeb;
  gap: 5%;
  border-radius: 10px;
`;

const TextContainer = styled.div`
  grid-column: 1/3;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5rem;
  font-weight: bold;
  background: black;
  color: white;
`;

const ImageContainer = styled.div<{ clicked: boolean }>`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: ${(props) => (props.clicked ? "#ee0260" : "white")};
  border-radius: 10px;
  cursor: pointer;
  &:active {
    margin-top: 5px;
    margin-left: 5px;
  }
`;

const Image = styled.img`
  width: 80%;
  height: 80%;
  object-fit: cover;
`;

const NextButton = styled.button`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 50%;
  height: 75px;
  background: white;
  border: none;
  border-radius: 10px;
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;
  &:active {
    font-weight: 900;
    background: #ee0260;
  }
`;

interface ArrayProps {
  category: string;
  handleLike: (category: string, product_num: number) => void;
  dataWhichIsArray: number[];
}

interface ItemOfSixProps {
  product_num: number;
  category: string;
  handleLike: (category: string, product_num: number) => void;
}

interface CategoryKey {
  0: string[];
  1: string[];
  2: string[];
  3: string[];
}

const ItemOfSix = ({ product_num, category, handleLike }: ItemOfSixProps) => {
  const publicUrl = process.env.PUBLIC_URL;
  const [clicked, setClicked] = useState(false);
  const handleClick = () => {
    setClicked(!clicked);
    handleLike(category, product_num);
  };

  useEffect(() => {
    setClicked(false);
  }, []);

  return (
    <ImageContainer onClick={handleClick} clicked={clicked}>
      <Image src={`${publicUrl}/img/${product_num}.jpg`} />
    </ImageContainer>
  );
};

const Six: React.FC<ArrayProps> = ({
  dataWhichIsArray,
  handleLike,
  category = "hood",
}) => {
  return (
    <ItemContainer>
      <TextContainer>
        {propMatcher[category as keyof propMatcherProps]}
      </TextContainer>
      {dataWhichIsArray.map((item: number) => (
        <ItemOfSix
          product_num={item}
          category={category}
          handleLike={handleLike}
        />
      ))}
    </ItemContainer>
  );
};

const Initialization = () => {
  const [nextClicked, setNextClicked] = React.useState(false);
  const [state, setState] = React.useState(0);
  const [data, setData] = React.useState<ItemProps>(emptyProps);
  const [liked, setLiked] = React.useState<ItemProps>(emptyProps);
  const [userId, setUserId] = React.useState("");

  const navigate = useNavigate();

  const searchApi = () => {
    axios
      .get("/api/initial-data")
      // .get("http://0.0.0.0:8001/initial-data/")
      .then((response) => {
        const temp = JSON.parse(response.data);
        for (const key in temp) {
          temp[key] = JSON.parse(temp[key]);
        }
        setData(temp);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    searchApi();
    getUser();
  }, []);

  const handleLike = (category: string, product_num: number) => {
    const temp = { ...liked };
    temp[category as keyof ItemProps].push(product_num);
    setLiked(temp);
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

  const handleNext = () => {
    // categories[state as keyof CategoryKey].forEach((value) => {
    //   if (liked[value as keyof ItemProps].length === 0) {
    //     console.log(liked[value as keyof ItemProps])
    //     setNextOK(false);
    //   } else {
    //     setNextOK(true);
    //   }
    // });
    setNextClicked(true);
    setTimeout(() => {
        setState(state + 1);
        setNextClicked(false);
      }, 1000);
    
  };

  useEffect(() => {
    if (state === 4) {
      navigate("/");
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
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [state]);

  const categories = {
    0: ["hood", "knit", "long", "polo"],
    1: ["shirt", "short", "sleeveless", "sweat"],
    2: ["cotton", "denim", "jogger", "jumper"],
    3: ["leggings", "shorts", "slacks", "etc"],
  };
  return (
    <>
      <LoginHeader />
      <BackGround>
        <InitHome nextClicked={nextClicked}>
          {state === 0 &&
            categories[state as keyof CategoryKey].map((category) => (
              <Six
                dataWhichIsArray={data[category as keyof ItemProps]}
                category={category}
                handleLike={handleLike}
              />
            ))}
          {state === 1 &&
            categories[state as keyof CategoryKey].map((category) => (
              <Six
                dataWhichIsArray={data[category as keyof ItemProps]}
                category={category}
                handleLike={handleLike}
              />
            ))}
          {state === 2 &&
            categories[state as keyof CategoryKey].map((category) => (
              <Six
                dataWhichIsArray={data[category as keyof ItemProps]}
                category={category}
                handleLike={handleLike}
              />
            ))}
          {state === 3 &&
            categories[state as keyof CategoryKey].map((category) => (
              <Six
                dataWhichIsArray={data[category as keyof ItemProps]}
                category={category}
                handleLike={handleLike}
              />
            ))}
        </InitHome>
        <NextButton onClick={handleNext}>
          CHOOSE ITEMS YOU LIKE AND CLICK HERE
        </NextButton>
      </BackGround>
    </>
  );
};

export default Initialization;
