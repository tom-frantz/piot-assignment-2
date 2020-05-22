import React, { useEffect, useState } from "react";
import axios from "axios";
import { Table, Space, Input, Button } from "antd";
import { SearchOutlined } from "@ant-design/icons";

interface CarsProps {}

export type Car = {
    car_number: string;
    make: string;
    body_type: string;
    seats: number;
    colour: string;
    latitude: number;
    longitude: number;
    cost_per_hour: number;
    lock_status: boolean;
    bookings: {
        booking_id: number;
        username: string;
        departure_time: string;
        return_time: string;
        created_at: string;
    }[];
};

interface UnformattedCar {
    car_number: string;
    make: string;
    body_type: string;
    seats: number;
    colour: string;
    latitude: string;
    longitude: string;
    cost_per_hour: string;
    lock_status: boolean;
    bookings: {
        booking_id: number;
        username: string;
        departure_time: string;
        return_time: string;
        created_at: string;
    }[];
}

const Cars: React.FC<CarsProps> = (props: CarsProps) => {
    const [cars, setCars] = useState<Car[]>([]);

    useEffect(() => {
        console.log("axios");
        axios.get("http://127.0.0.1:5000/cars/all").then((value: { data: UnformattedCar[] }) => {
            console.log(value.data);
            setCars(
                value.data.map(
                    ({
                        car_number,
                        make,
                        body_type,
                        bookings,
                        colour,
                        cost_per_hour,
                        latitude,
                        lock_status,
                        longitude,
                        seats,
                    }: UnformattedCar): Car => {
                        return {
                            car_number,
                            make,
                            body_type,
                            seats,
                            colour,
                            latitude: parseFloat(latitude),
                            longitude: parseFloat(longitude),
                            cost_per_hour: parseFloat(cost_per_hour),
                            lock_status,
                            bookings: [],
                        };
                    }
                )
            );
        });
    }, []);

    const getColumnSearchProps = (dataIndex: string) => ({
        filterDropdown: ({
            setSelectedKeys,
            selectedKeys,
            confirm,
            clearFilters,
        }: {
            setSelectedKeys: any;
            selectedKeys: any;
            confirm: any;
            clearFilters: any;
        }) => (
            <div style={{ padding: 8 }}>
                <Input
                    placeholder={`Search ${dataIndex}`}
                    value={selectedKeys[0]}
                    onChange={(e) => setSelectedKeys(e.target.value ? [e.target.value] : [])}
                    onPressEnter={() => handleSearch(selectedKeys, confirm, dataIndex)}
                    style={{ width: 188, marginBottom: 8, display: "block" }}
                />
                <Space>
                    <Button
                        type="primary"
                        onClick={() => handleSearch(selectedKeys, confirm, dataIndex)}
                        icon={<SearchOutlined />}
                        size="small"
                        style={{ width: 90 }}
                    >
                        Search
                    </Button>
                    <Button
                        onClick={() => handleReset(clearFilters)}
                        size="small"
                        style={{ width: 90 }}
                    >
                        Reset
                    </Button>
                </Space>
            </div>
        ),
        filterIcon: (filtered: unknown) => (
            <SearchOutlined style={{ color: filtered ? "#1890ff" : undefined }} />
        ),
        onFilter: (value: any, record: { [key: string]: any }) =>
            record[dataIndex].toString().toLowerCase().includes(value.toLowerCase()),
    });

    const handleSearch = (selectedKeys: string, confirm: () => {}, dataIndex: string) => {
        confirm();
    };

    const handleReset = (clearFilters: () => void) => {
        clearFilters();
    };

    return (
        <Table
            dataSource={cars}
            columns={[
                {
                    title: "Number Plate",
                    dataIndex: "car_number",
                    key: "numberPlate",
                    ...getColumnSearchProps("car_number"),
                },
                { title: "Make", dataIndex: "make", key: "make", ...getColumnSearchProps("make") },
                {
                    title: "Body Type",
                    dataIndex: "body_type",
                    key: "bodyType",
                    ...getColumnSearchProps("body_type"),
                },
                {
                    title: "Colour",
                    dataIndex: "colour",
                    key: "colour",
                    ...getColumnSearchProps("colour"),
                },
                {
                    title: "Seats",
                    dataIndex: "seats",
                    key: "seats",
                    ...getColumnSearchProps("seats"),
                },
                {
                    title: "Cost",
                    dataIndex: "cost_per_hour",
                    key: "cost",
                    ...getColumnSearchProps("cost_per_hour"),
                },
                {
                    title: "Actions",
                    key: "actions",
                    render: (text, record) => (
                        <Space>
                            <a>Book</a>
                        </Space>
                    ),
                },
            ]}
        />
    );
};

export default Cars;
