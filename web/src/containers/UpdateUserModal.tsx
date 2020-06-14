import React from "react";
import { Modal, Form, Input, Select } from "antd";
import { User } from "../screens/Users";

interface UpdateUserModalProps {
    visible: boolean;
    setVisible(visible: boolean): void;
    user?: User;
    onOk(values: any): void;
    showPasswordFields?: boolean;
}

const UpdateUserModal: React.FC<UpdateUserModalProps> = (props: UpdateUserModalProps) => {
    const { visible, setVisible, user, onOk, showPasswordFields } = props;

    const [form] = Form.useForm();
    form.setFields([
        { name: "username", value: user?.username },
        { name: "first_name", value: user?.first_name },
        { name: "last_name", value: user?.last_name },
        { name: "email", value: user?.email },
        { name: "role", value: user?.role },
    ]);

    return (
        <Modal
            visible={visible}
            onCancel={() => {
                setVisible(false);
                form.resetFields();
            }}
            onOk={() => {
                form.validateFields()
                    .then((values: any) => {
                        onOk(values);
                        setVisible(false);
                        form.resetFields();
                    })
                    .catch((info) => {
                        console.log("Validate Failed:", info);
                    });
            }}
        >
            <Form form={form}>
                <Form.Item name={"username"} label={"Username"}>
                    <Input disabled={user !== undefined} value={user?.username} />
                </Form.Item>
                <Form.Item name={"first_name"} label={"First Name"}>
                    <Input />
                </Form.Item>
                <Form.Item name={"last_name"} label={"Last Name"}>
                    <Input />
                </Form.Item>
                <Form.Item name={"email"} label={"Email"}>
                    <Input />
                </Form.Item>
                <Form.Item name={"role"} label={"Role"}>
                    <Select>
                        <Select.Option value={"admin"}>Admin</Select.Option>
                        <Select.Option value={"manager"}>Manager</Select.Option>
                        <Select.Option value={"engineer"}>Engineer</Select.Option>
                    </Select>
                </Form.Item>
                {showPasswordFields && [
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
                    </Form.Item>,
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
                    </Form.Item>,
                ]}
            </Form>
        </Modal>
    );
};

export default UpdateUserModal;
