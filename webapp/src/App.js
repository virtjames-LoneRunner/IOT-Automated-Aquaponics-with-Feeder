import "./App.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Footer from "./components/Footer";
import axios from "axios";

// Routes
import Home from "./routes/Home";
import Settings from "./routes/Settings";
import FeedingSchedules from "./routes/FeedingSchedules";
import UserDetails from "./routes/UserDetails";
import Actions from "./routes/Actions";

axios.defaults.headers.post["Accept"] = "application/json";
axios.defaults.headers.post["Content-Type"] = "application/json";
axios.defaults.headers["Cache-Control"] = "no-cache";
axios.defaults.headers["Pragma"] = "no-cache";
axios.defaults.headers["Expires"] = "0";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/settings",
    element: <Settings />,
  },
  {
    path: "/user-details",
    element: <UserDetails />,
  },
  {
    path: "/actions",
    element: <Actions />,
  },
  {
    path: "/feeding-schedules",
    element: <FeedingSchedules />,
  },
]);

function App() {
  return (
    <div className="App flex">
      <div className="bg-[#04080f] h-screen flex-1">
        <RouterProvider router={router} />
        <Footer />
      </div>
    </div>
  );
}

export default App;
