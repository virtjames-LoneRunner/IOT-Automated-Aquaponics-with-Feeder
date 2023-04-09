import axios from "axios";
import { BASE_URL } from "../config";

export default function FeedingSchedule({
  sched,
  setUpdateCount,
  updateCount,
}) {
  const handleDelete = (e) => {
    console.log(e.target);
    axios
      .delete(`${BASE_URL}/feeding-schedules?id=${e.target.name}`)
      .then((res) => {
        if (res.status === 200) {
          setUpdateCount(updateCount + 1);
        }
      });
  };
  return (
    <div className="bg-indigo-900/10 py-2 px-4 h-fit mb-2">
      <div className="text-left flex justify-between">
        <div>
          <span className="text-gray-500">{"Time: "}</span>
          <span className="text-lg text-blue-400 font-bold">
            {tConvert(sched.time_scheduled)}
          </span>
        </div>
        <div>
          <button onClick={handleDelete} name={sched.id}>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="w-6 h-6 pointer-events-none"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>
      <div className="text-left">
        <span className="text-gray-500">{"Feed Amount: "}</span>
        <span className="text-lg text-blue-400 font-bold">
          {sched.feed_amount}
        </span>
        <span className="text-blue-400">{" grams"}</span>
      </div>
      <div className="text-left">
        <span className="text-gray-500">{"Status: "}</span>
        <span className="text-lg text-blue-400 font-bold">
          {sched.done_for_the_day ? "Done" : "Upcoming"}
        </span>
      </div>
    </div>
  );
}
function tConvert(time) {
  // Check correct time format and split into components
  time = time.toString().match(/^([01]\d|2[0-3])(:)([0-5]\d)(:[0-5]\d)?$/) || [
    time,
  ];

  if (time.length > 1) {
    // If time format correct
    time = time.slice(1); // Remove full string match value
    time[5] = +time[0] < 12 ? " AM" : " PM"; // Set AM/PM
    time[0] = +time[0] % 12 || 12; // Adjust hours
  }
  return time.join(""); // return adjusted time or original string
}
