import React from "react";
import { Link, withRouter, useLocation } from "react-router-dom";
import { Menu } from "antd";
import jwt_decode from "jwt-decode";

interface NavbarProps {
    auth: string | null;
    setAuth(auth: undefined): void;
}

const AdminRoute = (props: NavbarProps) => {
    return [
        <Menu.Item key="/cars">
            <Link to={"/cars"}>Cars</Link>
        </Menu.Item>,
        <Menu.Item key="/users">
            <Link to={"/users"}>Users</Link>
        </Menu.Item>,
        <Menu.Item key="/bookings">
            <Link to={"/bookings"}>Bookings</Link>
        </Menu.Item>,
        <Menu.Item key="/map">
            <Link to={"/map"}>Map</Link>
        </Menu.Item>,
        <Menu.Item
            style={{ float: "right" }}
            key="logout"
            onClick={() => {
                props.setAuth(undefined);
            }}
        >
            Log out
        </Menu.Item>,
    ];
};

const ManagerRoute = (props: NavbarProps) => {
    return [
        <Menu.Item key={"/dashboard"}>
            <Link to={"/dashboard"}>Dashboard</Link>
        </Menu.Item>,
        <Menu.Item
            style={{ float: "right" }}
            key="logout"
            onClick={() => {
                props.setAuth(undefined);
            }}
        >
            Log out
        </Menu.Item>,
    ];
};

const EngineerRoute = (props: NavbarProps) => {
    return [
        <Menu.Item key={"/issues"}>
            <Link to={"/issues"}>Issues</Link>
        </Menu.Item>,
        <Menu.Item
            style={{ float: "right" }}
            key="logout"
            onClick={() => {
                props.setAuth(undefined);
            }}
        >
            Log out
        </Menu.Item>,
    ];
};

const Navbar: React.FC<NavbarProps> = (props: NavbarProps) => {
    const { auth } = props;
    let location = useLocation();
    console.log(location);

    let access_token_contents:
        | { identity: { username: string; role: string } }
        | undefined = undefined;
    if (auth) access_token_contents = jwt_decode(auth);

    return (
        <Menu theme="dark" mode="horizontal" selectedKeys={[location.pathname]}>
            {access_token_contents?.identity.role === "admin" && AdminRoute(props)}
            {access_token_contents?.identity.role === "manager" && ManagerRoute(props)}
            {access_token_contents?.identity.role === "engineer" && EngineerRoute(props)}
            {auth == null && [
                <Menu.Item key="/login">
                    <Link to={"/login"}>Login</Link>
                </Menu.Item>,
                <Menu.Item key="/register">
                    <Link to={"/register"}>Register</Link>
                </Menu.Item>,
            ]}
        </Menu>
    );
};

export default Navbar;
