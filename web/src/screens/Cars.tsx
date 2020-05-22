import React, { useEffect, useState } from "react";
import axios from "axios";
import Moment from "moment";
import { Space, Table, Modal, DatePicker, Alert } from "antd";
import { Car, formatCars, getColumnSearchProps, UnformattedCar } from "../utils/tableUtils";

const { RangePicker } = DatePicker;

interface CarsProps {}

const Cars: React.FC<CarsProps> = (props: CarsProps) => {
    const [cars, setCars] = useState<Car[]>([]);
    const [visible, setVisible] = useState<boolean>(false);
    const [error, setError] = useState<string | undefined>(undefined);
    const [alert, setAlert] = useState<string | undefined>();

    const [selectedRange, setSelectedRange] = useState<[Moment.Moment, Moment.Moment]>();
    const [selectedCar, setSelectedCar] = useState<Car | undefined>(undefined);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/cars/all").then((value: { data: UnformattedCar[] }) => {
            setCars(value.data.map(formatCars));
        });
    }, []);

    return (
        <div style={{ display: "flex", flexDirection: "column" }}>
            <Modal
                visible={visible}
                onCancel={() => setVisible(false)}
                onOk={() => {
                    for (const booking of (selectedCar as Car).bookings) {
                        if (
                            Moment(booking.departure_time) <=
                                (selectedRange as [Moment.Moment, Moment.Moment])[1] &&
                            Moment(booking.return_time) >=
                                (selectedRange as [Moment.Moment, Moment.Moment])[0]
                        ) {
                            setError("You can't use that date period");
                            return;
                        }
                    }
                    console.log(
                        (selectedRange as [Moment.Moment, Moment.Moment])[0].format("YYYY-MM-DD") +
                            "/" +
                            (selectedRange as [Moment.Moment, Moment.Moment])[1].format(
                                "YYYY-MM-DD"
                            )
                    );

                    axios
                        .post("http://127.0.0.1:5000/bookings/new", {
                            car_number: (selectedCar as Car).car_number,
                            booking_period:
                                (selectedRange as [Moment.Moment, Moment.Moment])[0].format(
                                    "YYYY-MM-DD"
                                ) +
                                "/" +
                                (selectedRange as [Moment.Moment, Moment.Moment])[1].format(
                                    "YYYY-MM-DD"
                                ),
                        })
                        .then((res) => setAlert(res.data.message))
                        .catch((err) => setAlert(err.message));

                    setVisible(false);
                }}
            >
                <RangePicker
                    disabledDate={(current) => {
                        for (const booking of (selectedCar as Car).bookings) {
                            if (
                                Moment(booking.departure_time) <= current &&
                                current <= Moment(booking.return_time)
                            ) {
                                return true;
                            }
                        }
                        // Can not select days before today and today
                        return current && current < Moment().endOf("day");
                    }}
                    value={selectedRange}
                    onChange={(values) => {
                        console.log(values);
                        setError(undefined);
                        // @ts-ignore
                        setSelectedRange(values);
                    }}
                />
                {error && <p style={{ color: "#F00" }}>{error}</p>}
            </Modal>
            {alert && <Alert message={alert} type="warning" closable onClose={() => {}} />}
            <Table
                dataSource={cars}
                columns={[
                    {
                        title: "Number Plate",
                        dataIndex: "car_number",
                        key: "numberPlate",
                        ...getColumnSearchProps("car_number"),
                    },
                    {
                        title: "Make",
                        dataIndex: "make",
                        key: "make",
                        ...getColumnSearchProps("make"),
                    },
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
                                    <a
                                        onClick={() => {
                                            setVisible(true);
                                            setSelectedCar(record);
                                        }}
                                    >
                                        Book
                                    </a>
                                </Space>
                            );
                        },
                    },
                ]}
            />
        </div>
    );
};

export default Cars;
