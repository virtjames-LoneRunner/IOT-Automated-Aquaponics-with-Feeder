import './App.css';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Footer from "./components/Footer";
import axios from 'axios'

// Routes
import Home from './routes/Home';
import Settings from './routes/Settings';
import FeedingSchedules from './routes/FeedingSchedules';


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
    path: '/user-details',
    element: <div className='flex text-white text-2xl items-center h-full justify-center'><h2 className='mb-24'>Coming Soon!</h2></div>
  },
  {
    path: "/actions",
    element: <div className='flex text-white text-2xl items-center h-full justify-center'><h2 className='mb-24'>Coming Soon!</h2></div>
  },
  {
    path: '/feeding-schedules',
    element: <FeedingSchedules />
  }
]);

function App() {
  return (
    <div className="App flex">
      <div className="bg-[#04080f] h-screen flex-1">
        <RouterProvider  router={router}/>
        <Footer />
      </div>
    </div>
  );
}

export default App;
