import { useEffect, useState } from "react";
import axios from "axios";

import { BASE_URL } from "../config";

export default function Home() {
  const [data, setData] = useState({
    date_time: "",
    dissolved_oxygen: 0,
    humidity: 0,
    pH_level: 0,
    temperature: 0,
    water_level: 0,
  });
  useEffect(() => {
    setInterval(function () {
      axios.get(`${BASE_URL}/dashboard`).then((res) => {
        if (res.status === 200) {
          setData(res.data.data);
        }
      });
    }, 5000);
  }, []);

  return (
    <div className="text-white h-full">
      <div className="shadow-[#5761ec] shadow-sm py-2 fixed top-0 w-full bg-[#04080f]">
        <h2 className="text-xl">Dashboard</h2>
      </div>
      <div className="grid grid-cols-2 gap-2 mt-12 h-4/6 px-5 py-4 fixed w-full">
        <div className="bg-indigo-900/10 flex flex-col justify-center items-center col-span-2">
          <h1 className="text-[#5761ec] text-xl mb-2">
            {new Date(data.date_time).toLocaleDateString()}{" "}
            {new Date(data.date_time).toLocaleTimeString()}
          </h1>
          <h2 className="text-gray-500 text-lg">Time Recorded</h2>
        </div>
        <div className="bg-indigo-900/10 flex flex-col justify-center items-center">
          <h1 className="text-[#5761ec] text-4xl mb-2">
            {data.temperature} °C
          </h1>
          <h2 className="text-gray-500 text-lg">Temperature</h2>
        </div>
        <div className="bg-indigo-900/10 flex flex-col justify-center items-center">
          <h1 className="text-[#5761ec] text-4xl mb-2">{data.water_level} m</h1>
          <h2 className="text-gray-500 text-lg">Water Level</h2>
        </div>
        <div className="bg-indigo-900/10 flex flex-col justify-center items-center">
          <h1 className="text-[#5761ec] text-4xl mb-2">{data.pH_level}</h1>
          <h2 className="text-gray-500 text-lg">pH Level</h2>
        </div>
        <div className="bg-indigo-900/10 flex flex-col justify-center items-center">
          <h1 className="text-[#5761ec] text-4xl mb-2">
            {data.dissolved_oxygen}
          </h1>
          <h2 className="text-gray-500 text-lg">Dissolved Oxygen</h2>
        </div>
      </div>
    </div>
  );
}
