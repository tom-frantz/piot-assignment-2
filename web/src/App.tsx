import React, { Dispatch, SetStateAction, useEffect, useState } from "react";
import "antd/dist/antd.css";
import "react-date-range/dist/styles.css"; // main style file
import "react-date-range/dist/theme/default.css"; // theme css file

import { Route, Router, Switch, Redirect } from "react-router-dom";
import { createBrowserHistory } from "history";
import { Layout } from "antd";
import axios from "axios";

import Login from "./screens/Login";
import Cars from "./screens/Cars";
import Navbar from "./containers/Navbar";
import PrivateRoute from "./containers/PrivateRoute";
import Register from "./screens/Register";
import Bookings from "./screens/Bookings";
import MyMap from "./screens/MyMap";
import Dashboard from "./screens/Dashboard";
import Issues from "./screens/Issues";
import Users from "./screens/Users";

const { Content, Header, Footer } = Layout;

const history = createBrowserHistory();

export const getAuthTimer = () => {
    return Math.floor(new Date().getTime() / 1000) + (15 * 60 - 1);
};

type FullAuth = { access_token: string; refresh_token: string; timeout: number };

export type Auth = FullAuth | undefined;

function AppNavigator() {
    const [auth, setAuthFn] = useState<Auth>(undefined);

    const setAuth = (auth: Auth) => {
        if (auth && auth.refresh_token) {
            localStorage.setItem("refresh_token", auth.refresh_token);
        }

        if (auth === undefined) {
            localStorage.removeItem("refresh_token");
        }

        setAuthFn(auth);
    };

    useEffect(() => {
        const interceptor = axios.interceptors.request.use(async (config) => {
            if (auth === undefined) return config;

            let accessToken = undefined;
            if (!("timeout" in auth) || Math.round(new Date().getTime() / 1000) >= auth.timeout) {
                const res = await axios
                    .create()
                    .post(
                        "http://127.0.0.1:5000/auth/refresh",
                        {},
                        { headers: { Authorization: `Bearer ${auth.refresh_token}` } }
                    );

                if (res.data.access_token) {
                    setAuth({
                        refresh_token: auth.refresh_token,
                        access_token: res.data.access_token,
                        timeout: getAuthTimer(),
                    });
                    accessToken = res.data.access_token;
                } else {
                    console.warn(res);
                    setAuth(undefined);
                    return Promise.reject("You must log in again.");
                }
            } else {
                console.log("No need for redo");
            }

            if (accessToken === undefined) accessToken = (auth as FullAuth).access_token;

            if (accessToken !== undefined) config.headers.Authorization = `Bearer ${accessToken}`;

            return config;
        });

        return () => {
            axios.interceptors.request.eject(interceptor);
        };
    });

    useEffect(() => {
        const refresh_token = localStorage.getItem("refresh_token");

        if (refresh_token) {
            axios
                .create()
                .post(
                    "http://127.0.0.1:5000/auth/refresh",
                    {},
                    { headers: { Authorization: `Bearer ${refresh_token}` } }
                )
                .then((values: any) => {
                    setAuth({
                        refresh_token: values.data.refresh_token as string,
                        access_token: values.data.access_token as string,
                        timeout: getAuthTimer(),
                    });
                })
                .catch((e) => {
                    console.error(e);
                    localStorage.removeItem("refresh_token");
                });
        }
    }, []);

    return (
        <Router history={history}>
            <Layout style={{ minHeight: "100vh" }}>
                <Header>
                    <Navbar auth={auth?.access_token || null} setAuth={setAuth} />
                </Header>
                <Content style={{ display: "flex", flexGrow: 1, justifyContent: "center" }}>
                    <Switch>
                        <Route path={"/"} exact>
                            {auth ? <Redirect to={"/cars"} /> : <Redirect to={"/login"} />}
                        </Route>
                        <Route path={"/login"} exact>
                            {!auth ? <Login setAuth={setAuth} /> : <Redirect to={"/cars"} />}
                        </Route>
                        <Route path={"/register"} exact>
                            {!auth ? <Register setAuth={setAuth} /> : <Redirect to={"/cars"} />}
                        </Route>
                        <PrivateRoute
                            access_token={auth?.access_token || null}
                            role={"admin"}
                            path={"/cars"}
                            exact
                        >
                            <Cars />
                        </PrivateRoute>
                        <PrivateRoute
                            access_token={auth?.access_token || null}
                            role={"admin"}
                            path={"/users"}
                            exact
                        >
                            <Users />
                        </PrivateRoute>
                        <PrivateRoute
                            access_token={auth?.access_token || null}
                            role={"admin"}
                            path={"/bookings"}
                            exact
                        >
                            <Bookings />
                        </PrivateRoute>
                        <PrivateRoute
                            access_token={auth?.access_token || null}
                            role={"admin"}
                            path={"/map"}
                            exact
                        >
                            <MyMap />
                        </PrivateRoute>

                        <PrivateRoute
                            access_token={auth?.access_token || null}
                            role={"engineer"}
                            path={"/issues"}
                            exact
                        >
                            <Issues auth={auth} />
                        </PrivateRoute>

                        <PrivateRoute
                            access_token={auth?.access_token || null}
                            role={"manager"}
                            path={"/dashboard"}
                            exact
                        >
                            <Dashboard />
                        </PrivateRoute>
                    </Switch>
                </Content>
                <Footer>Hey hey hey hey hey</Footer>
            </Layout>
        </Router>
    );
}

export default AppNavigator;
