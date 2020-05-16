import React from "react";
import { Link, withRouter, useLocation } from "react-router-dom";
import { Menu } from "antd";

interface NavbarProps {
    auth: boolean;
    setAuth(auth: undefined): void;
}

const Navbar: React.FC<NavbarProps> = (props: NavbarProps) => {
    const { auth } = props;
    let location = useLocation();
    console.log(location);

    return (
        <Menu theme="dark" mode="horizontal" selectedKeys={[location.pathname]}>
            {auth && [
                <Menu.Item key="/cars">
                    <Link to={"/cars"}>Cars</Link>
                </Menu.Item>,
                <Menu.Item
                    key="something"
                    onClick={() => {
                        props.setAuth(undefined);
                    }}
                >
                    Log out
                </Menu.Item>,
            ]}
            {!auth && [
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
