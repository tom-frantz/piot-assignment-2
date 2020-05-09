import React, { SetStateAction, useEffect } from "react";
import { Button, Form, Input } from "antd";
import { Auth } from "../App";
import axios from "axios";
import { withRouter, RouteComponentProps } from "react-router-dom";

interface LoginProps extends RouteComponentProps<{}> {
    setAuth(authValue: undefined | Partial<Auth>): void;
}

const Login: React.FC<LoginProps> = (props: LoginProps) => {
    const [form] = Form.useForm();

    const onFinish = (values: { username: string; password: string }): void => {
        axios
            .post("http://127.0.0.1:5000/auth/new", values)
            .then((res) => {
                props.setAuth({
                    access_token: res.data.access_token,
                    refresh_token: res.data.refresh_token,
                });
                props.history.push("/cars");
            })
            .catch((error) => {
                if (error.response) {
                    // The request was made and the server responded with a status code
                    // that falls out of the range of 2xx
                    if (error.response.status === 401) {
                        form.setFields([
                            {
                                name: "username",
                                errors: ["The username or password is incorrect!"],
                            },
                            {
                                name: "password",
                                errors: ["The username or password is incorrect!"],
                            },
                        ]);
                    }
                } else if (error.request) {
                    // The request was made but no response was received
                    // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                    // http.ClientRequest in node.js
                    console.log(error.request);
                } else {
                    // Something happened in setting up the request that triggered an Error
                    console.log("Error", error.message);
                }
                console.log(error.config);
            });
    };

    return (
        <Form form={form} onFinish={onFinish as (values: unknown) => void} style={{ padding: 13 }}>
            <Form.Item
                name={"username"}
                label={"Username"}
                rules={[{ required: true, message: "Username is required" }]}
            >
                <Input />
            </Form.Item>
            <Form.Item
                label={"Password"}
                name={"password"}
                rules={[{ required: true, message: "Password is required" }]}
                hasFeedback
            >
                <Input.Password />
            </Form.Item>
            <Form.Item>
                <Button type="primary" htmlType="submit">
                    Submit
                </Button>
            </Form.Item>
        </Form>
    );
};

export default withRouter(Login);
