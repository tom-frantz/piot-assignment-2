import React, { useEffect, useState } from "react";
import axios from "axios";
import api from "../utils/api";
import { Booking, Car, formatBookings, getColumnSearchProps } from "../utils/tableUtils";
import { Space, Table, Button } from "antd";
import UpdateUserModal from "../containers/UpdateUserModal";

interface UsersProps {}

export interface User {
    username: string;
    first_name: string;
    last_name: string;
    email: string;
    role: string;
    bookings: Booking[];
}

const Users: React.FC<UsersProps> = (props: UsersProps) => {
    const [users, setUsers] = useState<User[]>([]);
    const [loading, setLoading] = useState(false);

    const [updateVisible, setUpdateVisible] = useState(false);
    const [createVisible, setCreateVisible] = useState(false);
    const [selectedUser, setSelectedUser] = useState<User | undefined>(undefined);

    console.log(users);

    const updateUsers = () => {
        setLoading(true);
        axios
            .get(`http://${api}:5000/users/all`)
            .then((values) => {
                setUsers(
                    values.data.map(
                        ({ username, first_name, last_name, email, role, bookings }: any) => ({
                            username,
                            first_name,
                            last_name,
                            email,
                            role,
                            bookings: bookings.map(formatBookings),
                        })
                    )
                );
                setLoading(false);
            })
            .catch();
    };

    useEffect(() => updateUsers(), []);

    return (
        <div style={{ display: "flex", flexDirection: "column" }}>
            <UpdateUserModal
                visible={updateVisible}
                setVisible={setUpdateVisible}
                user={selectedUser as User}
                onOk={(values: Exclude<User, "bookings">) => {
                    axios.put(`http://${api}:5000/users/update`, values).then(() => updateUsers());
                }}
            />
            <UpdateUserModal
                visible={createVisible}
                setVisible={setCreateVisible}
                onOk={({
                    username,
                    first_name,
                    last_name,
                    email,
                    role,
                    password,
                }: Exclude<User, "bookings"> & { password: string }) => {
                    axios
                        .post(`http://${api}:5000/users/register`, {
                            username,
                            first_name,
                            last_name,
                            email,
                            role,
                            password,
                        })
                        .then(() => updateUsers());
                }}
                showPasswordFields
            />
            <Button onClick={() => setCreateVisible(true)} style={{ margin: 20 }} type={"primary"}>
                Create New User
            </Button>
            <Table
                loading={loading}
                dataSource={users}
                columns={[
                    {
                        title: "Username",
                        dataIndex: "username",
                        key: "username",
                        ...getColumnSearchProps("username"),
                    },
                    {
                        title: "First Name",
                        dataIndex: "first_name",
                        key: "first_name",
                        ...getColumnSearchProps("first_name"),
                    },
                    {
                        title: "Last Name",
                        dataIndex: "last_name",
                        key: "last_name",
                        ...getColumnSearchProps("last_name"),
                    },
                    {
                        title: "Email",
                        dataIndex: "email",
                        key: "email",
                        ...getColumnSearchProps("email"),
                    },
                    {
                        title: "Role",
                        dataIndex: "role",
                        key: "role",
                        ...getColumnSearchProps("role"),
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
                                                setSelectedUser(record);
                                                setUpdateVisible(true);
                                            }}
                                        >
                                            Update
                                        </a>
                                    </div>
                                    <div style={{ display: "flex", flexDirection: "column" }}>
                                        <a onClick={() => {}}>Delete</a>
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

export default Users;
