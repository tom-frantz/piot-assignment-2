import React from "react";
import { Route, Redirect, RouteProps } from "react-router-dom";

interface PrivateRouteProps extends RouteProps {
    auth: boolean;
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
                auth ? (
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
