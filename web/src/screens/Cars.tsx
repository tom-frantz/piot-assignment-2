import React, { useEffect, useState } from "react";
import axios from "axios";
import { Table, Space, Input, Button } from "antd";
import { SearchOutlined } from "@ant-design/icons";

interface CarsProps {}

export type Car = {
    number_plate: string;
    make: string;
    body_type: string;
    colour: string;
    seats: number;
    location: [number, number];
    cost: number;
};

const Cars: React.FC<CarsProps> = (props: CarsProps) => {
    const [searchText, setSearchText] = useState<string>("");
    const [searchedColumn, setSearchedColumn] = useState<string>("");

    const [cars, setCars] = useState<Car[]>([
        {
            number_plate: "sqb981",
            make: "RX-8",
            body_type: "sports",
            colour: "red",
            seats: 4,
            location: [0, 0],
            cost: 100,
        },
        {
            number_plate: "sqb981",
            make: "RX-9",
            body_type: "sports",
            colour: "red",
            seats: 4,
            location: [0, 0],
            cost: 100,
        },
        {
            number_plate: "sqb981",
            make: "RX-8",
            body_type: "sports",
            colour: "green",
            seats: 4,
            location: [0, 0],
            cost: 100,
        },
    ]);

    useEffect(() => {
        console.log("axios");
        axios.get("http://127.0.0.1:5000/cars/available").then((value: { data: Car[] }) => {
            console.log(value.data);
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
        setSearchedColumn(dataIndex);
        setSearchText(selectedKeys[0]);
    };

    const handleReset = (clearFilters: () => void) => {
        clearFilters();
        setSearchText("");
    };

    return (
        <Table
            dataSource={cars}
            columns={[
                {
                    title: "Number Plate",
                    dataIndex: "number_plate",
                    key: "numberPlate",
                    ...getColumnSearchProps("number_plate"),
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
                { title: "Cost", dataIndex: "cost", key: "cost", ...getColumnSearchProps("cost") },
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
