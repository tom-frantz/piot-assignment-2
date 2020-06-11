import React from "react";
import Iframe from "react-iframe";

interface DashboardProps {}

const Dashboard: React.FC<DashboardProps> = (props: DashboardProps) => {
    return (
        <Iframe
            width="900px"
            height="700px"
            url="https://datastudio.google.com/embed/reporting/7c6932cb-ea7d-4120-8a3e-aca0941892c0/page/4quTB"
            // frameBorder="0"
            //@ts-ignore
            // style="border:0"
            allowFullScreen
        />
    );
};

export default Dashboard;
