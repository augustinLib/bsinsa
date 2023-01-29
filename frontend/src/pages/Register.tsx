import axios from "axios";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";
import LoginHeader from "../components/Login/LoginHeader";

export const RegisterBackground = styled.div`
  display: flex;
  flex: 1;
  justify-content: center;
  align-items: center;
  background: #ebebeb;
  min-width: 1000px;
`;

export const RegisterBlock = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: 2fr 1.5fr 1.5fr 2fr;
  align-items: center;

  width: 30vw;
  height: 60vh;

  border-radius: 20px;
  background: #ffffff;
  }
`;

export const InfoInput = styled.input`
  width: 80%;
  height: 50%;
  display: flex;
  margin: 0 auto;
  margin-top: 10px;
  margin-bottom: 10px;
  border: 2px solid #ebebeb;
  border-radius: 10px;
  padding-left: 10px;
  font-size: 20px;
`;

export const InfoRegister = styled.button`
  width: 80%;
  height: 40%;
  display: flex;
  margin: 0 auto;
  margin-top: 10px;
  margin-bottom: 10px;
  border: 2px solid #ebebeb;
  border-radius: 10px;
  padding-left: 10px;
  font-size: 20px;

  font-size: 20px;
  background: black;
  color: white;
  align-items: center;
  justify-content: center;

  &:hover {
    color: red;
  }
`;

const Register = () => {
  const [id, setId] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const onChangeId = (e: React.ChangeEvent<HTMLInputElement>) => {
    setId(e.target.value);
  };

  const onChangePassword = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    axios
      .post("/api/register", { id, password })
      .then((response) => {
        if (response.status === 200) {
          sessionStorage.setItem("token", response.data);
          alert("회원가입이 완료되었습니다.");
          navigate("/login");
        }
      })
      .catch((err) => {
        if (err.response.status === 501) {
          alert("중복된 ID입니다.");
          navigate("/register");
        } else {
          alert("회원가입에 실패하였습니다. 다시 시도해주세요.");
          navigate("/register");
        }
      });
  };

  return (
    <>
      <LoginHeader />
      <RegisterBackground>
        <form onSubmit={handleSubmit}>
          <RegisterBlock>
            <h1>SIGNIN</h1>
            <InfoInput
              type="text"
              id="id"
              placeholder="Username"
              onChange={onChangeId}
            />
            <InfoInput
              type="password"
              id="password"
              placeholder="Password"
              onChange={onChangePassword}
            />
            <InfoRegister type="submit">REGISTER</InfoRegister>
          </RegisterBlock>
        </form>
      </RegisterBackground>
    </>
  );
};

export default Register;
