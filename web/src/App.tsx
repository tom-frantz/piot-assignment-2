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
import Bookings from "./screens/Bookings";

const { Content, Header, Footer } = Layout;

const history = createBrowserHistory();

export const getAuthTimer = () => {
    return Math.floor(new Date().getTime() / 1000) + (15 * 60 - 1);
};

type FullAuth = { access_token: string; refresh_token: string; timeout: number };

export type Auth = FullAuth | { refresh_token: string } | undefined;

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
        console.log("HEY AUTH");
        console.log(refresh_token);
        if (refresh_token) setAuthFn({ refresh_token });
    }, []);

    return (
        <Router history={history}>
            <Layout style={{ height: "100vh" }}>
                <Header>
                    <Navbar auth={auth !== undefined} setAuth={setAuth} />
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
                        <PrivateRoute auth={auth !== undefined} path={"/cars"} exact>
                            <Cars />
                        </PrivateRoute>
                        <PrivateRoute auth={auth !== undefined} path={"/bookings"} exact>
                            <Bookings />
                        </PrivateRoute>
                    </Switch>
                </Content>
                <Footer>Hey hey hey hey hey</Footer>
            </Layout>
        </Router>
    );
}

export default AppNavigator;
