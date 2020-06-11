import React, { useEffect, useState } from "react";
import { Button, Input, Space, Table } from "antd";
import {
    Booking,
    formatBookings,
    getColumnSearchProps,
    UnformattedBooking,
} from "../utils/tableUtils";
import axios from "axios";

interface BookingsProps {}

const Bookings: React.FC<BookingsProps> = (props: BookingsProps) => {
    const [bookings, setBookings] = useState<Booking[]>([]);

    const updateBookings = () => {
        axios
            .get("http://127.0.0.1:5000/bookings/me")
            .then((value: { data: UnformattedBooking[] }) => {
                setBookings(value.data.map(formatBookings));
            });
    };

    useEffect(() => {
        updateBookings();
    }, []);

    const cancelBooking = (bookingID: number) => {
        axios
            .delete("http://127.0.0.1:5000/bookings/cancel/" + bookingID.toString())
            .then(() => updateBookings());
    };

    return (
        <Table
            dataSource={bookings}
            columns={[
                {
                    title: "Car Number",
                    dataIndex: "car_number",
                    key: "Car Number",
                    ...getColumnSearchProps("car_number"),
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
                {
                    title: "Actions",
                    key: "actions",
                    render: (text, record: Booking) => {
                        return (
                            <Space style={{ flexDirection: "column", alignItems: "flex-start" }}>
                                <a>See Car</a>
                                {new Date() <= record.departure_time && (
                                    <a onClick={() => cancelBooking(record.booking_id)}>
                                        Cancel Booking
                                    </a>
                                )}
                            </Space>
                        );
                    },
                },
            ]}
        />
    );
};

export default Bookings;
