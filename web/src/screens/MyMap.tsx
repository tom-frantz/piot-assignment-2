import React, { useEffect, useState } from "react";
import { GoogleApiWrapper, Map, Marker, Circle, InfoWindow } from "google-maps-react";
import axios from "axios";
import { Car, formatCars, UnformattedCar } from "../utils/tableUtils";

interface MapProps {
    google: any;
}

const MyMap: React.FC<MapProps> = (props: MapProps) => {
    const [cars, setCars] = useState<Car[]>([]);

    const [activeMarker, setActiveMarker] = useState(undefined);
    const [activeCar, setActiveCar] = useState<Car | undefined>(undefined);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/cars/all").then((value: { data: UnformattedCar[] }) => {
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
                console.log(car);

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

export default GoogleApiWrapper({ apiKey: "AIzaSyA251T6B4lBT15MrIlRF4wDAeWe4wnyKgA" })(MyMap);
