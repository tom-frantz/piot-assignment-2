import React, { useEffect, useState } from "react";
import { Car, formatCars, UnformattedCar } from "../utils/tableUtils";
import axios from "axios";
import { GoogleApiWrapper, InfoWindow, Map, Marker } from "google-maps-react";
import api from "../utils/api";

interface IssuesProps {
    google: any;
}

const Issues: React.FC<IssuesProps> = (props: IssuesProps) => {
    const [cars, setCars] = useState<Car[]>([]);

    const [activeMarker, setActiveMarker] = useState(undefined);
    const [activeCar, setActiveCar] = useState<Car | undefined>(undefined);

    useEffect(() => {
        axios.get(`http://${api}/cars/all`).then((value: { data: UnformattedCar[] }) => {
            setCars(value.data.map(formatCars));
        });
    }, []);

    return (
        <Map
            google={props.google}
            // zoom={14}
            style={{ height: "75%", width: "75%", left: "-37.5%" }}
            initialCenter={{
                lat: -37.8136,
                lng: 144.9631,
            }}
        >
            {cars.map((car: Car) => {
                return (
                    <Marker
                        // @ts-ignore
                        position={{ lat: car.latitude, lng: car.longitude }}
                        onClick={(props: any, marker: any, e: any) => {
                            setActiveMarker(marker);
                            setActiveCar(car);
                        }}
                        name={car.car_number}
                    />
                );
            })}
            <InfoWindow
                marker={activeMarker}
                visible={activeMarker !== undefined}
                // @ts-ignore
                onClose={() => {
                    setActiveMarker(undefined);
                }}
            >
                <div>{activeCar && <h4>{activeCar.car_number}</h4>}</div>
            </InfoWindow>
        </Map>
    );
};

export default GoogleApiWrapper({ apiKey: "AIzaSyA251T6B4lBT15MrIlRF4wDAeWe4wnyKgA" })(Issues);
