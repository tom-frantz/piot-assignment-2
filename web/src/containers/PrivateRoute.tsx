import React from "react";
import { Route, Redirect, RouteProps } from "react-router-dom";

interface PrivateRouteProps extends RouteProps {}

const PrivateRoute: React.FC<PrivateRouteProps> = ({ children, ...rest }: PrivateRouteProps) => {
    return (
        <Route
            {...rest}
            render={({ location }) =>
                false ? (
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
