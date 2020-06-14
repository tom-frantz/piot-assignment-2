import React from "react";
import { Car, getColumnSearchProps } from "../utils/tableUtils";
import { Modal, Space, Table } from "antd";

interface ViewCarHistoryProps {
    visible: boolean;
    setVisible(visible: boolean): void;
    car?: Car;
}

const ViewCarHistoryModal: React.FC<ViewCarHistoryProps> = (props: ViewCarHistoryProps) => {
    const { visible, setVisible, car } = props;
    return (
        <Modal visible={visible} onOk={() => setVisible(false)} onCancel={() => setVisible(false)}>
            <h1>Bookings for {car?.car_number}</h1>
            <Table
                dataSource={car?.bookings || []}
                columns={[
                    {
                        title: "ID",
                        dataIndex: "booking_id",
                        key: "booking_id",
                        ...getColumnSearchProps("booking_id"),
                    },
                    {
                        title: "User",
                        dataIndex: "username",
                        key: "username",
                        ...getColumnSearchProps("username"),
                    },
                    {
                        title: "From",
                        dataIndex: "departure_time",
                        key: "from",
                        ...getColumnSearchProps("departure_time"),
                        render: (text, record) => {
                            return (
                                <Space>
                                    <p style={{ marginBottom: 0 }}>
                                        {record.departure_time.toLocaleDateString()}
                                    </p>
                                </Space>
                            );
                        },
                    },
                    {
                        title: "To",
                        dataIndex: "return_time",
                        key: "to",
                        ...getColumnSearchProps("return_time"),
                        render: (text, record) => {
                            return (
                                <Space>
                                    <p style={{ marginBottom: 0 }}>
                                        {record.return_time.toLocaleDateString()}
                                    </p>
                                </Space>
                            );
                        },
                    },
                    {
                        title: "Created At",
                        dataIndex: "created_at",
                        key: "createdAt",
                        ...getColumnSearchProps("created_at"),
                        render: (text, record) => {
                            return (
                                <Space>
                                    <p style={{ marginBottom: 0 }}>
                                        {record.created_at.toLocaleTimeString()},{" "}
                                        {record.created_at.toLocaleDateString()}
                                    </p>
                                </Space>
                            );
                        },
                    },
                ]}
            />
        </Modal>
    );
};

export default ViewCarHistoryModal;
