import React from "react";
import { Route, Redirect, RouteProps } from "react-router-dom";

interface PrivateRouteProps extends RouteProps {
    auth: undefined | string;
}

const PrivateRoute: React.FC<PrivateRouteProps> = ({
    children,
    auth,
    ...rest
}: PrivateRouteProps) => {
    return (
        <Route
            {...rest}
            render={() =>
                auth !== undefined ? (
                    children
                ) : (
                    <Redirect
                        to={{
                            pathname: "/login",
                        }}
                    />
                )
            }
        />
    );
};

export default PrivateRoute;
