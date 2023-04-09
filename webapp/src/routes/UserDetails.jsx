import axios from "axios";
import { useEffect, useState } from "react";
import { BASE_URL } from "../config";

export default function UserDetails() {
  const [userData, setUserData] = useState({});

  useEffect(() => {
    axios.get(`${BASE_URL}/user-details`).then((res) => {
      if (res.status === 200) {
        setUserData(res.data.user_details);
      }
    });
  }, []);

  const handleInput = (e) => {
    setUserData({
      ...userData,
      [e.target.name]: e.target.value,
    });
  };

  const handleUpdateOrAdd = (e) => {
    axios
      .post(`${BASE_URL}/user-details?id=${e.target.name}`, userData)
      .then((res) => {
        if (res.status === 200) {
          console.log(200);
        }
      });
  };

  return (
    <div className="text-white h-full">
      <div className="shadow-[#5761ec] shadow-sm py-2 fixed top-0 w-full bg-[#04080f]">
        <h2 className="text-xl">User Details</h2>
      </div>
      <div className="mt-12 h-5/6 px-5 pt-4 pb-9">
        <div className="bg-indigo-900/10 py-2 px-4 text-left space-y-3">
          <h2>User Mobile:</h2>
          <input
            type="text"
            className="custom-input"
            name="mobile_number"
            defaultValue={userData.mobile_number}
            onChange={handleInput}
          />
          <div>
            <button
              type="submit"
              className="bg-blue-800 w-full py-1 rounded-md"
              onClick={handleUpdateOrAdd}
              name={userData.id}
            >
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
