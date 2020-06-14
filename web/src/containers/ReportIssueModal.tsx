import React from "react";
import { Modal, Form, Input, Button, message } from "antd";
import { Car } from "../utils/tableUtils";
import axios from "axios";
import api from "../utils/api";

interface ReportIssueModalProps {
    visible: boolean;
    setVisible(visible: boolean): void;
    car?: Car;
    onOk(): void;
}

const ReportIssueModal: React.FC<ReportIssueModalProps> = (props: ReportIssueModalProps) => {
    const { visible, setVisible, car, onOk } = props;

    const [form] = Form.useForm();
    form.setFields([{ name: "carNumber", value: car?.car_number }]);

    console.warn(car);

    const onFinish = ({ carNumber, issue }: { carNumber: string; issue: string }) => {
        axios
            .post(`http://${api}:5000/issues/new`, {
                car_number: carNumber,
                description: issue,
            })
            .then(() => {
                message.success(`The issue for car "${carNumber}" was successfully posted`);
                setVisible(false);
                form.resetFields();
                onOk();
            })
            .catch((error) => {
                message.error("There was an error with your request. Please try again");
                console.error(error);
            });
    };

    return (
        <Modal
            visible={visible}
            onCancel={() => {
                setVisible(false);
                form.resetFields();
            }}
            onOk={() => {
                form.validateFields()
                    .then((values) => {
                        onFinish(values as any);
                    })
                    .catch((info) => {
                        console.log("Validate Failed:", info);
                    });
            }}
        >
            <Form form={form} onFinish={onFinish as any} style={{ paddingTop: 20 }}>
                <Form.Item
                    label={"Car number"}
                    name={"carNumber"}
                    rules={[{ required: true, message: "Car is required" }]}
                >
                    <Input disabled={true} value={car?.car_number} />
                </Form.Item>
                <Form.Item
                    label={"Issue"}
                    name={"issue"}
                    rules={[
                        { required: true, message: "The issue description is required" },
                        { min: 1, message: "The issue description is required" },
                    ]}
                >
                    <Input />
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default ReportIssueModal;
