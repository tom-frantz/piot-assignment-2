import React from "react";
import { Layout, Form, Input, Button } from "antd";

interface RegisterProps {}

const Register: React.FC<RegisterProps> = (props: RegisterProps) => {
    const [form] = Form.useForm();

    const onFinish = ({ username, first_name, last_name, email, password }: any) => {
        fetch("http://127.0.0.1:5000/users/register", {
            method: "POST",
            body: JSON.stringify({
                username,
                first_name,
                last_name,
                email,
                password,
            }),
            redirect: "follow",
        })
            .then((response: any) => response.json())
            .then((result: any) => console.log(result))
            .catch((error: any) => console.log("error", error));
    };

    return (
        <Form form={form} onFinish={onFinish} style={{ padding: 13 }}>
            <Form.Item
                label={"Username"}
                name={"username"}
                rules={[
                    { required: true, message: "Username is required" },
                    { min: 3, message: "Must be at least three characters long" },
                    { max: 15, message: "Must be at most 15 characters long" },
                ]}
            >
                <Input />
            </Form.Item>
            <Form.Item
                label={"First Name"}
                name={"first_name"}
                rules={[
                    { required: true, message: "First Name is required" },
                    { min: 3, message: "Must be at least three characters long" },
                    { max: 15, message: "Must be at most 15 characters long" },
                ]}
            >
                <Input />
            </Form.Item>
            <Form.Item
                label={"Last Name"}
                name={"last_name"}
                rules={[
                    { required: true, message: "Last Name is required" },
                    { min: 3, message: "Must be at least three characters long" },
                    { max: 15, message: "Must be at most 15 characters long" },
                ]}
            >
                <Input />
            </Form.Item>
            <Form.Item
                label={"Password"}
                name={"password"}
                rules={[
                    { required: true, message: "Password is required" },
                    { min: 3, message: "Must be at least three characters long" },
                    { max: 15, message: "Must be at most 15 characters long" },
                ]}
                hasFeedback
            >
                <Input.Password />
            </Form.Item>
            <Form.Item
                name="confirm"
                label="Confirm Password"
                dependencies={["password"]}
                hasFeedback
                rules={[
                    {
                        required: true,
                        message: "Please confirm your password",
                    },
                    ({ getFieldValue }) => ({
                        validator(rule, value) {
                            if (!value || getFieldValue("password") === value) {
                                return Promise.resolve();
                            }
                            return Promise.reject(
                                "The two passwords that you entered do not match"
                            );
                        },
                    }),
                ]}
            >
                <Input.Password />
            </Form.Item>

            <Form.Item
                name="email"
                label="E-mail"
                rules={[
                    {
                        type: "email",
                        message: "The input is not valid E-mail",
                    },
                    {
                        required: true,
                        message: "Please input your E-mail",
                    },
                ]}
            >
                <Input />
            </Form.Item>
            <Form.Item>
                <Button type="primary" htmlType="submit">
                    Submit
                </Button>
            </Form.Item>
        </Form>
    );
};

export default Register;
