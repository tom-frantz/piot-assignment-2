import React, { Dispatch, SetStateAction, useEffect, useState } from "react";
import "antd/dist/antd.css";
import { Route, Router, Switch, Redirect } from "react-router-dom";
import { createBrowserHistory } from "history";
import { Layout } from "antd";
import axios from "axios";

import Login from "./screens/Login";
import Cars from "./screens/Cars";
import Navbar from "./containers/Navbar";
import PrivateRoute from "./containers/PrivateRoute";
import Register from "./screens/Register";

const { Content, Header, Footer } = Layout;

const history = createBrowserHistory();

const getTimer = () => {
    return Math.floor(new Date().getTime() / 1000) + (15 * 60 - 1);
};

export type Auth = { access_token: string; refresh_token: string };

function AppNavigator() {
    const [auth, setAuthFunction] = useState<undefined | Auth>(undefined);
    const [timeout, setTimeoutFunc] = useState<undefined | number>(undefined);

    useEffect(() => {
        const interceptor = axios.interceptors.request.use(async (config) => {
            if (auth === undefined) return config;

            let accessToken = undefined;

            if (timeout && Math.round(new Date().getTime() / 1000) >= timeout) {
                console.log("WE DOING THE REDO THING");
                const res = await axios
                    .create()
                    .post(
                        "http://127.0.0.1:5000/auth/refresh",
                        {},
                        { headers: { Authorization: `Bearer ${auth.refresh_token}` } }
                    );

                if (res.data.access_token) {
                    setAuth({ access_token: res.data.access_token });
                    accessToken = res.data.access_token;
                    setTimeoutFunc(getTimer);
                } else {
                    console.warn(res);
                    setAuth(undefined);
                    setTimeoutFunc(undefined);
                    return Promise.reject("Uh oh");
                }
            } else {
                console.log("No need for redo");
            }

            if (accessToken === undefined) accessToken = auth.access_token;

            if (accessToken !== undefined)
                config.headers.Authorization = `Bearer ${auth.access_token}`;

            return config;
        });

        return () => {
            axios.interceptors.request.eject(interceptor);
        };
    });

    const setAuth = (authValue: Partial<Auth> | undefined) => {
        if (authValue === undefined) {
            setTimeoutFunc(undefined);
            setAuthFunction(undefined);
            return;
        } else if (authValue.refresh_token) {
            setTimeoutFunc(getTimer());
        }

        if (authValue.refresh_token && authValue.access_token) {
            console.log("doing");
            setAuthFunction(authValue as Auth);
        } else if (authValue.refresh_token) {
            // AuthValue is just refresh token
            setAuthFunction({
                refresh_token: authValue.refresh_token,
                access_token: (auth as Auth).access_token,
            });
        }
    };

    return (
        <Router history={history}>
            <Layout style={{ height: "100vh" }}>
                <Header>
                    <Navbar auth={auth !== undefined} />
                </Header>
                <Content style={{ display: "flex", flexGrow: 1, justifyContent: "center" }}>
                    <Switch>
                        <Route path={"/"} exact>
                            {auth ? <Redirect to={"/cars"} /> : <Redirect to={"/login"} />}
                        </Route>
                        <Route path={"/login"} exact>
                            <Login setAuth={setAuth} />
                        </Route>
                        <Route path={"/register"} exact>
                            <Register setAuth={setAuth} />
                        </Route>
                        <PrivateRoute auth={auth !== undefined} path={"/cars"} exact>
                            <Cars />
                        </PrivateRoute>
                    </Switch>
                </Content>
                <Footer>Hey hey hey hey hey</Footer>
            </Layout>
        </Router>
    );
}

export default AppNavigator;
