import React from "react";
import { Modal, Form, Input, InputNumber, Select, message } from "antd";
import { Car } from "../utils/tableUtils";
import axios from "axios";
import api from "../utils/api";

interface UpdateModalProps {
    visible: boolean;
    setVisible(visible: boolean): void;
    car?: Car;
    onOk(values: any): void;
}

const UpdateCarModal: React.FC<UpdateModalProps> = (props: UpdateModalProps) => {
    const { visible, setVisible, car, onOk } = props;

    const [form] = Form.useForm();
    form.setFields([
        { name: "car_number", value: car?.car_number },
        { name: "make", value: car?.make },
        { name: "body_type", value: car?.body_type },
        { name: "seats", value: car?.seats },
        { name: "colour", value: car?.colour },
        { name: "latitude", value: car?.latitude },
        { name: "longitude", value: car?.longitude },
        { name: "cost_per_hour", value: car?.cost_per_hour },
        { name: "lock_status", value: car?.lock_status ? "True" : "False" },
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
            <Form form={form} style={{ paddingTop: 20 }} labelCol={{ span: 6 }}>
                <Form.Item name={"car_number"} label={"Car Number"}>
                    <Input disabled={car !== undefined} value={car?.car_number} />
                </Form.Item>
                <Form.Item name={"make"} label={"Make"}>
                    <Input />
                </Form.Item>
                <Form.Item name={"body_type"} label={"Body Type"}>
                    <Input />
                </Form.Item>
                <Form.Item name={"seats"} label={"Seats"}>
                    <InputNumber />
                </Form.Item>
                <Form.Item name={"colour"} label={"Colour"}>
                    <Input />
                </Form.Item>
                <Form.Item name={"latitude"} label={"Latitude"}>
                    <InputNumber style={{ width: 200 }} />
                </Form.Item>
                <Form.Item name={"longitude"} label={"Longitude"}>
                    <InputNumber style={{ width: 200 }} />
                </Form.Item>
                <Form.Item name={"cost_per_hour"} label={"Cost Per Hour"}>
                    <InputNumber />
                </Form.Item>
                <Form.Item name={"lock_status"} label={"Lock Status"}>
                    <Select>
                        <Select.Option value={"True"}>True</Select.Option>
                        <Select.Option value={"False"}>False</Select.Option>
                    </Select>
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default UpdateCarModal;
