import React from "react";
import "antd/dist/antd.css";
import { Route, Router, Switch } from "react-router-dom";
import { createBrowserHistory } from "history";
import { Layout } from "antd";
import Login from "./screens/Login";
import Cars from "./screens/Cars";
import Navbar from "./containers/Navbar";
import PrivateRoute from "./containers/PrivateRoute";

const { Content, Header, Footer } = Layout;

const history = createBrowserHistory();

function AppNavigator() {
    return (
        <Router history={history}>
            <Layout style={{ height: "100vh" }}>
                <Header>
                    <Navbar />
                </Header>
                <Content style={{ display: "flex", flexGrow: 1 }}>
                    <Switch>
                        <Route path={"/"} exact>
                            <Login />
                        </Route>
                        <Route path={"/login"} exact>
                            <Login />
                        </Route>
                        <PrivateRoute path={"/cars"} exact>
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
