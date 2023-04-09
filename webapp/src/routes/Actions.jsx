import axios from "axios";
import { useEffect, useState } from "react";
import { BASE_URL } from "../config";

export default function Actions() {
  const [actions, setActions] = useState([]);
  useEffect(() => {
    setInterval(function () {
      axios.get(`${BASE_URL}/actions`).then((res) => {
        if (res.status === 200) {
          setActions(res.data.actions);
        }
      });
    }, 5000);
  }, []);

  return (
    <div className="text-white h-full">
      <div className="shadow-[#5761ec] shadow-sm py-2 fixed top-0 w-full bg-[#04080f]">
        <h2 className="text-xl">Actions</h2>
      </div>
      <div className="mt-12 h-5/6 px-5 py-4 overflow-y-auto">
        {actions.length > 0 ? (
          actions.map((action) => (
            <div
              className="bg-indigo-900/10 py-2 px-4 h-fit mb-2 text-left"
              key={action.id}
              id={action.id}
            >
              <div>
                <span class="text-xs text-gray-400">Date Added: </span>
                <span class="text-xs">
                  {new Date(action.datetime_added).toLocaleDateString()}{" "}
                  {new Date(action.datetime_added).toLocaleTimeString()}
                </span>
              </div>
              <div>
                <span class="text-xs text-gray-400">Date Executed: </span>
                <span class="text-xs">
                  {new Date(action.datetime_executed).toLocaleDateString()}{" "}
                  {new Date(action.datetime_executed).toLocaleTimeString()}
                </span>
              </div>
              <div className="text-left">
                <span className="text-xs text-gray-400">{"Status: "}</span>
                <span className="text-xs text-blue-400 font-bold">
                  {action.done_executing ? "Done" : "Upcoming"}
                </span>
              </div>
              <div className="w-full bg-blue-600/5 my-2">
                <table className="table-auto w-full">
                  {/* <h2 className="text-xs">Actions:</h2> */}
                  <tr>
                    <th className="text-xs">Feeder Motor</th>
                    <th className="text-xs">Pump</th>
                    <th className="text-xs">Solenoid (inlet)</th>
                    <th className="text-xs">Solenoid (outlet)</th>
                  </tr>
                  <tr>
                    <td className="text-xs">{action.turns} turns</td>
                    <td className="text-xs">
                      {action.pump === 1 ? "ON" : "OFF"}
                    </td>
                    <td className="text-xs">
                      {action.sol_in === 1 ? "ON" : "OFF"}
                    </td>
                    <td className="text-xs">
                      {action.sol_out === 1 ? "ON" : "OFF"}
                    </td>
                  </tr>
                </table>
              </div>
              <div>
                <div className="text-xs text-gray-400">Remarks:</div>
                <p className="text-xs text-gray-400 bg-blue-600/5 p-2 mt-1">
                  {action.cause}
                </p>
              </div>
            </div>
          ))
        ) : (
          <div>Loading Actions</div>
        )}
      </div>
    </div>
  );
}
