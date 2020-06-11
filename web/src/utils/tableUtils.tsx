import { Button, Input, Space } from "antd";
import React from "react";
import { SearchOutlined } from "@ant-design/icons";

export interface Car {
    car_number: string;
    make: string;
    body_type: string;
    seats: number;
    colour: string;
    latitude: number;
    longitude: number;
    cost_per_hour: number;
    lock_status: boolean;
    bookings: Booking[];
    issues: Issue[];
}

export interface Booking {
    booking_id: number;
    username: string;
    car_number: string;
    departure_time: Date;
    return_time: Date;
    created_at: Date;
}

export const getColumnSearchProps = (dataIndex: string) => ({
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

export interface UnformattedIssues {
    description: string;
    issue_id: number;
    status: boolean;
}

export interface UnformattedCar {
    car_number: string;
    make: string;
    body_type: string;
    seats: number;
    colour: string;
    latitude: string;
    longitude: string;
    cost_per_hour: string;
    lock_status: boolean;
    bookings?: UnformattedBooking[];
    issues?: UnformattedIssues[];
}

export interface UnformattedBooking {
    booking_id: number;
    created_at: string;
    departure_time: string;
    return_time: string;
    username: string;
    car_number: string;
}

export const formatBookings = ({
    username,
    booking_id,
    created_at,
    departure_time,
    return_time,
    car_number,
}: UnformattedBooking): Booking => ({
    username,
    booking_id,
    created_at: new Date(created_at + "Z"),
    departure_time: new Date(departure_time + "Z"),
    return_time: new Date(return_time + "Z"),
    car_number,
});

export interface Issue {
    description: string;
    issue_id: number;
    status: boolean;
}

export const formatIssues = ({ description, issue_id, status }: UnformattedIssues): Issue => ({
    description,
    issue_id,
    status,
});

export const formatCars = ({
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
    issues,
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
        issues: (issues || []).map(formatIssues),
        bookings: (bookings || []).map(formatBookings),
    };
};
