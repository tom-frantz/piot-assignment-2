import React, { useState } from "react";
import Moment from "moment";
import { Alert, DatePicker, Modal } from "antd";

import axios from "axios";
import api from "../utils/api";
import { Car } from "../utils/tableUtils";
import ReactAddToCalendar from "react-add-to-calendar";

const { RangePicker } = DatePicker;

interface BookingModalProps {
    visible: boolean;
    setVisible(visible: boolean): void;
    onOk(): void;
    car?: Car;
}

const BookingModal: React.FC<BookingModalProps> = (props: BookingModalProps) => {
    const { visible, setVisible, onOk, car: selectedCar } = props;

    const [alert, setAlert] = useState<string | undefined>();
    const [selectedRange, setSelectedRange] = useState<[Moment.Moment, Moment.Moment]>();
    const [error, setError] = useState<string | undefined>(undefined);

    return (
        <>
            {alert && (
                <Alert
                    type="warning"
                    closable
                    onClose={() => {}}
                    message={
                        <div>
                            <p>Your booking has been added</p>
                            <ReactAddToCalendar
                                event={{
                                    title: "Car Booking",
                                    startTime: (selectedRange as [
                                        Moment.Moment,
                                        Moment.Moment
                                    ])[0].toISOString(),
                                    endTime: (selectedRange as [
                                        Moment.Moment,
                                        Moment.Moment
                                    ])[1].toISOString(),
                                    description: "Your booking time.",
                                }}
                            />
                        </div>
                    }
                />
            )}
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

                    axios
                        .post(`http://${api}:5000/bookings/new`, {
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
                        .then((res) => {
                            setAlert(res.data.message);
                            onOk();
                        })
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
        </>
    );
};

export default BookingModal;
