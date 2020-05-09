import React, { SetStateAction, useEffect } from "react";
import { Button, Form, Input } from "antd";
import { Auth } from "../App";
import axios from "axios";

interface LoginProps {
    setAuth(authValue: undefined | Partial<Auth>): void;
}

const Login: React.FC<LoginProps> = (props: LoginProps) => {
    const [form] = Form.useForm();

    const onFinish = (values: { username: string; password: string }): void => {
        axios
            .post("http://127.0.0.1:5000/auth/new", values)
            .then((res) =>
                props.setAuth({
                    access_token: res.data.access_token,
                    refresh_token: res.data.refresh_token,
                })
            );
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

export default Login;
