import React, { useEffect, useState } from "react";
import axios from "axios";
import { Button, message, Space, Table } from "antd";
import { Car, formatCars, getColumnSearchProps, UnformattedCar } from "../utils/tableUtils";
import api from "../utils/api";
import BookingModal from "../containers/BookingModal";
import ReportIssueModal from "../containers/ReportIssueModal";
import UpdateCarModal from "../containers/UpdateCarModal";
import ViewCarHistoryModal from "../containers/ViewCarHistoryModal";

interface CarsProps {}

const Cars: React.FC<CarsProps> = (props: CarsProps) => {
    const [cars, setCars] = useState<Car[]>([]);

    // Modal visibilities
    const [bookingVisible, setBookingVisible] = useState<boolean>(false);
    const [issuesVisible, setIssuesVisible] = useState<boolean>(false);
    const [createCarVisible, setCreateCarVisible] = useState(false);
    const [updateCarVisible, setUpdateCarVisible] = useState<boolean>(false);
    const [carHistoryVisible, setCarHistoryVisible] = useState<boolean>(false);

    const [loading, setLoading] = useState(false);

    const [selectedCar, setSelectedCar] = useState<Car | undefined>(undefined);

    const deleteCar = (record: Car) => {
        axios
            .delete(`http://${api}:5000/cars/delete/${record.car_number}`)
            .then(() => message.success("Car was successfully deleted"))
            .catch((e) => {
                console.error(e);
            });
    };

    const updateCars = () => {
        setLoading(true);
        axios.get(`http://${api}:5000/cars/all`).then((value: { data: UnformattedCar[] }) => {
            setCars(value.data.map(formatCars));
            setLoading(false);
        });
    };

    useEffect(() => {
        updateCars();
    }, []);

    return (
        <div style={{ display: "flex", flexDirection: "column" }}>
            <BookingModal
                visible={bookingVisible}
                setVisible={setBookingVisible}
                onOk={updateCars}
                car={selectedCar}
            />
            <ReportIssueModal
                visible={issuesVisible}
                setVisible={setIssuesVisible}
                car={selectedCar}
                onOk={updateCars}
            />
            <UpdateCarModal
                visible={updateCarVisible}
                setVisible={setUpdateCarVisible}
                car={selectedCar}
                onOk={(values) => {
                    values.lock_status = values.lock_status === "True";

                    axios
                        .put(`http://${api}:5000/cars/update`, values)
                        .then(() => {
                            message.success(
                                `The car "${values.car_number}" was successfully updated`
                            );
                            updateCars();
                        })
                        .catch((error) => {
                            message.error("There was an error with your request. Please try again");
                            console.error(error);
                        });
                }}
            />
            <UpdateCarModal
                visible={createCarVisible}
                setVisible={setCreateCarVisible}
                onOk={(values) => {
                    values.lock_status = values.lock_status === "True";

                    axios
                        .post(`http://${api}:5000/cars/new`, values)
                        .then(() => {
                            message.success(
                                `The car "${values.car_number}" was successfully created`
                            );
                            updateCars();
                        })
                        .catch((error) => {
                            message.error("There was an error with your request. Please try again");
                            console.error(error);
                        });
                }}
            />
            <ViewCarHistoryModal
                visible={carHistoryVisible}
                setVisible={setCarHistoryVisible}
                car={selectedCar}
            />

            <Button
                onClick={() => setCreateCarVisible(true)}
                style={{ margin: 20 }}
                type={"primary"}
            >
                Create New Car
            </Button>

            <Table
                loading={loading}
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
                            return (
                                <Space>
                                    <div
                                        style={{
                                            display: "flex",
                                            marginRight: 20,
                                            flexDirection: "column",
                                        }}
                                    >
                                        <a
                                            onClick={() => {
                                                setSelectedCar(record);
                                                setBookingVisible(true);
                                            }}
                                        >
                                            Book
                                        </a>
                                        <a
                                            onClick={() => {
                                                setSelectedCar(record);
                                                setIssuesVisible(true);
                                            }}
                                        >
                                            Report Issue
                                        </a>
                                        <a
                                            onClick={() => {
                                                setSelectedCar(record);
                                                setCarHistoryVisible(true);
                                            }}
                                        >
                                            See Bookings
                                        </a>
                                    </div>
                                    <div style={{ display: "flex", flexDirection: "column" }}>
                                        <a
                                            onClick={() => {
                                                setSelectedCar(record);
                                                setUpdateCarVisible(true);
                                            }}
                                        >
                                            Update Details
                                        </a>
                                        <a onClick={() => deleteCar(record)}>Delete</a>
                                    </div>
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
