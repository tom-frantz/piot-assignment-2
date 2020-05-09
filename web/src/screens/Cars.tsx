import React, { useEffect } from "react";
import axios from "axios";

interface CarsProps {}

const Cars: React.FC<CarsProps> = (props: CarsProps) => {
    useEffect(() => {
        console.log("axios");
        axios.get("http://127.0.0.1:5000/users/me");
    }, []);

    return <p>Cars</p>;
};

export default Cars;
