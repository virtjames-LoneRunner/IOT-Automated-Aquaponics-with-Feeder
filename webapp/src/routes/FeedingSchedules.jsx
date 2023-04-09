import axios from "axios"
import { useEffect, useState } from "react"
import { BASE_URL } from "../config"
import FeedingSchedule from "../components/FeedingSchedule"



export default function FeedingSchedules() {
    const [feedingSchedules, setFeedingSchedules] = useState([])
    const [schedule_input, setScheduleInput] = useState({})

    const [updateCount, setUpdateCount] = useState(0)

    useEffect(() => {
        axios.get(`${BASE_URL}/feeding-schedules`).then((response) => {
            if (response.status === 200) {
                setFeedingSchedules(response.data.schedules)
            }
        })
    }, [updateCount])

    const handleInput = (e) => {
        setScheduleInput({
            ...schedule_input,
            [e.target.name] : e.target.value
        })
    }

    const handleAddSchedule = (e) => {
        e.preventDefault()
        axios.post(`${BASE_URL}/feeding-schedules`, schedule_input).then(res => {
            if (res.status === 200) {
                setUpdateCount(updateCount + 1)
                e.target.reset()
            }
        })  
    }

    return (
        <div className="text-white h-full" >
            <div className="shadow-[#5761ec] shadow-sm py-2 fixed top-0 w-full bg-[#04080f]">
                <h2 className="text-xl">Feeding Schedules</h2>
            </div>
            <div className="mt-12 h-5/6 px-5 pt-4 pb-9 flex flex-col justify-between">
                <div className="grid grid-cols-1 gap-2 h-full overflow-y-auto">
                    {feedingSchedules.map((sched) => (
                        <FeedingSchedule sched={sched}/>
                    ))}
                </div>
                <form onSubmit={handleAddSchedule} className="bg-indigo-900/10 py-2 px-4 text-left space-y-3">
                    <div className="flex flex-col space-y-1">
                        <h2>Time:</h2>
                        <input onChange={handleInput} className="custom-input" type="time" name="time_scheduled" />
                    </div>
                        <div className="flex flex-col space-y-1">
                            <h2>Feeds Amount:</h2>
                            <input onChange={handleInput} className="custom-input" type="number" name="feed_amount" />
                        </div>
                    <div>
                        <button type="submit" className="bg-blue-800 w-full py-1 rounded-md">
                            Add Schedule
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}