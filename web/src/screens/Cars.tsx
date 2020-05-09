import React, { useEffect, useState } from "react";
import axios from "axios";

interface CarsProps {}

const Cars: React.FC<CarsProps> = (props: CarsProps) => {
    const [name, setName] = useState();

    useEffect(() => {
        console.log("axios");
        axios.get("http://127.0.0.1:5000/users/me").then(
            (value: {
                data: {
                    first_name: string;
                    last_name: string;
                    email: string;
                    username: string;
                };
            }) => {
                const { username, first_name, last_name, email } = value.data;

                console.log(value.data);
                setName(first_name);
            }
        );
    }, []);

    return <p>{name}</p>;
};

export default Cars;
