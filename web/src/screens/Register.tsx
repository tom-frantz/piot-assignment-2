import React from "react";
import { Layout, Form, Input, Button } from "antd";

const { Content } = Layout;

interface RegisterProps {}

const Register: React.FC<RegisterProps> = (props: RegisterProps) => {
    // username password firstname lastname email
    const [form] = Form.useForm();

    const onFinish = (values: unknown) => {
        console.log("Success:", values);
        form.setFields([{ name: "username", errors: ["The username is already in use"] }]);

        // TODO form
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
                name={"firstName"}
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
                name={"lastName"}
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
                    { required: true, message: "Username is required" },
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
                        message: "Please confirm your password!",
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
