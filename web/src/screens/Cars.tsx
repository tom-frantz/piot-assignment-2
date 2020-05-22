import React, { useEffect, useState } from "react";
import axios from "axios";
import { Space, Table } from "antd";
import { Car, formatCars, getColumnSearchProps, UnformattedCar } from "../utils/tableUtils";

interface CarsProps {}

const Cars: React.FC<CarsProps> = (props: CarsProps) => {
    const [cars, setCars] = useState<Car[]>([]);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/cars/all").then((value: { data: UnformattedCar[] }) => {
            setCars(value.data.map(formatCars));
        });
    }, []);

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
                    render: (text, record) => {
                        console.log(text, record);

                        return (
                            <Space>
                                <a>Book</a>
                            </Space>
                        );
                    },
                },
            ]}
        />
    );
};

export default Cars;
