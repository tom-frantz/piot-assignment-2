import React from "react";
import { Link, withRouter } from "react-router-dom";
import { Menu } from "antd";

interface NavbarProps {
    auth: boolean;
}

const Navbar: React.FC<NavbarProps> = (props: NavbarProps) => {
    const { auth } = props;

    return (
        <Menu theme="dark" mode="horizontal">
            {auth && [
                <Menu.Item key="/cars">
                    <Link to={"/cars"}>Cars</Link>
                </Menu.Item>,
                <Menu.Item key="something">Log out</Menu.Item>,
            ]}
        </Menu>
    );
};

export default Navbar;
