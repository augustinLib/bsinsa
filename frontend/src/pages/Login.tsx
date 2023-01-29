import React from "react";
import LoginHeader from "../components/Login/LoginHeader";
import {
  RegisterBackground,
  RegisterBlock,
  InfoInput,
  InfoRegister,
} from "./Register";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import styled from "styled-components";

const LoginBlock = styled(RegisterBlock)`
grid-template-columns: 1fr;
grid-template-rows: 2fr 1.5fr 1.5fr 0.5fr 1fr 1fr 1.2fr;

height: 70vh;
}
`;

const NavigateSignUp = styled(InfoRegister)`
  height: 90%;
  background-color: #f2f2f2;
  color: black;
`;

const InfoLogin = styled(InfoRegister)`
  height: 90%;
`;

const Login = () => {
  const [id, setId] = React.useState("");
  const [password, setPassword] = React.useState("");

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
      .post("/api/login", { id, password })
      .then((response) => {
        if (response.status === 200) {
          sessionStorage.setItem("token", id);
          alert("로그인이 완료되었습니다.");
          navigate("/");
        }
      })
      .catch((err) => {
        if (err.response.status === 502) {
          alert("아이디 또는 비밀번호가 일치하지 않습니다.");
          navigate("/login");
        } else {
          console.log(err.response);
          alert("로그인에 실패하였습니다. 다시 시도해주세요.");
          navigate("/login");
        }
      });
  };

  return (
    <>
      <LoginHeader />
      <RegisterBackground>
        <form onSubmit={handleSubmit}>
          <LoginBlock>
            <h1>LOGIN</h1>
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
            <span></span>
            <InfoLogin type="submit">LOGIN</InfoLogin>
            <NavigateSignUp onClick={() => navigate("/register")}>
              SIGNUP
            </NavigateSignUp>
          </LoginBlock>
        </form>
      </RegisterBackground>
    </>
  );
};

export default Login;
