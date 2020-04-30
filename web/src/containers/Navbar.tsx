import React from "react";
import { Link, withRouter } from "react-router-dom";
import { Menu } from "antd";

interface NavbarProps {
    location: {
        pathname: string;
    };
}

const Navbar: React.FC<NavbarProps> = (props: NavbarProps) => {
    const {
        location: { pathname },
    } = props;

    return (
        <Menu theme="dark" mode="horizontal">
            {(pathname !== "/" || true) && [
                <Menu.Item key="/cars">
                    <Link to={"/cars"}>Cars</Link>
                </Menu.Item>,
                <Menu.Item key="something">Log out</Menu.Item>,
            ]}
        </Menu>
    );
};

export default withRouter((props) => <Navbar {...props} />);
