import React, { useEffect, useState } from "react";
import { Route, Redirect, RouteProps } from "react-router-dom";
import jwt_decode from "jwt-decode";

interface PrivateRouteProps extends RouteProps {
    access_token: string | null;
    role?: string;
}

const PrivateRoute: React.FC<PrivateRouteProps> = ({
    children,
    access_token,
    role,
    ...rest
}: PrivateRouteProps) => {
    const [timerDone, setTimerDone] = useState(false);

    useEffect(() => {
        const timeout = setTimeout(() => setTimerDone(true), 3000);
        return () => {
            clearTimeout(timeout);
        };
    }, []);

    let access_token_contents:
        | { identity: { username: string; role: string } }
        | undefined = undefined;
    if (access_token) access_token_contents = jwt_decode(access_token);

    const access_granted =
        access_token && (role === undefined || role === access_token_contents?.identity?.role);
    return (
        <Route
            {...rest}
            render={() =>
                access_granted ? (
                    children
                ) : (
                    <>
                        {!timerDone && <h1>You do not have access</h1>}
                        {timerDone && (
                            <Redirect
                                to={{
                                    pathname: "/login",
                                }}
                            />
                        )}
                    </>
                )
            }
        />
    );
};

export default PrivateRoute;
