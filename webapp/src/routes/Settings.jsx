import axios from "axios"
import { useEffect, useState } from "react"
import { BASE_URL } from "../config"


export default function Settings() {
    const [settings, setSettings] = useState({
        // default_feed_amount: 0.00,
        // min_temperature: 0.00,
        // max_temperature: 0.00,
        // min_water_level: 0.00,
        // max_water_level: 0.00,
        // pH_level: 0.00,
        // DO_level: 0.00,
    })
    const [message, setMessage] = useState("")
    useEffect(() => {
        axios.get(`${BASE_URL}/settings`).then((response) => {if (response.status === 200) {
            setSettings(response.data.settings_data)
        }})
    }, [])

    const handleSubmit = (e) => {
        e.preventDefault()
        // console.log(settings)
        axios.post(`${BASE_URL}/settings`, settings).then((res) => {
            if (res.status === 200) {
                setMessage(res.data.message)

                setTimeout(() => {
                    setMessage("")
                }, 2000)
            }
        })
    }

    const handleInput = (e) => {
        setSettings({
            ...settings,
            [e.target.name]: parseFloat(e.target.value)
        })
    }

    return (
        <div className="text-white h-full" >
            <div className="shadow-[#5761ec] shadow-sm py-2 fixed top-0 w-full bg-[#04080f]">
                <h2 className="text-xl">Settings</h2>
            </div>
            <form className="mt-16 h-5/6 px-5 py-4 space-y-5" onSubmit={handleSubmit} method="post">
                <div className="bg-indigo-900/10 py-2 px-4">
                    <h2 className="text-left text-[#5761ec] mb-2">Default Feed Amount</h2>
                    <div className="flex items-center space-x-2">
                        <input onChange={handleInput} type="number" name="default_feed_amount" defaultValue={settings.default_feed_amount} className="text-white bg-[#04080f] focus:outline-none px-2 py-2 w-full"/>
                        <h2>grams</h2>
                    </div>
                </div>
                <div className="flex space-x-2">
                    <div className="bg-indigo-900/10 py-2 px-4">
                        <h2 className="text-left text-[#5761ec] mb-2">Min Temperature</h2>
                        <div className="flex items-center space-x-2">
                            <input onChange={handleInput} type="number" name="min_temperature" defaultValue={settings.min_temperature} className="text-white bg-[#04080f] focus:outline-none px-2 py-2 w-full"/>
                            <h2>°C</h2>
                        </div>
                    </div>
                    <div className="bg-indigo-900/10 py-2 px-4">
                        <h2 className="text-left text-[#5761ec] mb-2">Max Temperature</h2>
                        <div className="flex items-center space-x-2">
                            <input onChange={handleInput} type="number" name="max_temperature" defaultValue={settings.max_temperature} className="text-white bg-[#04080f] focus:outline-none px-2 py-2 w-full"/>
                            <h2>°C</h2>
                        </div>
                    </div>
                </div>
                <div className="flex space-x-2">
                    <div className="bg-indigo-900/10 py-2 px-4">
                        <h2 className="text-left text-[#5761ec] mb-2">Min Water Level</h2>
                        <div className="flex items-center space-x-2">
                            <input onChange={handleInput} type="number" name="min_water_level" defaultValue={settings.min_water_level} className="text-white bg-[#04080f] focus:outline-none px-2 py-2 w-full"/>
                            <h2>m</h2>
                        </div>
                    </div>
                    <div className="bg-indigo-900/10 py-2 px-4">
                        <h2 className="text-left text-[#5761ec] mb-2">Max Water Level</h2>
                        <div className="flex items-center space-x-2">
                            <input onChange={handleInput} type="number" name="max_water_level" defaultValue={settings.max_water_level} className="text-white bg-[#04080f] focus:outline-none px-2 py-2 w-full"/>
                            <h2>m</h2>
                        </div>
                    </div>
                </div>
                <div className="bg-indigo-900/10 py-2 px-4">
                    <h2 className="text-left text-[#5761ec] mb-2">Desired pH Level</h2>
                    <input onChange={handleInput} type="number" name="pH_level" defaultValue={settings.pH_level} className="text-white bg-[#04080f] focus:outline-none px-2 py-2 w-full"/>
                </div>
                <div className="bg-indigo-900/10 py-2 px-4">
                    <h2 className="text-left text-[#5761ec] mb-2">Desired Dissolved Oxygen Level</h2>
                    <input onChange={handleInput} type="number" name="DO_level" defaultValue={settings.DO_level} className="text-white bg-[#04080f] focus:outline-none px-2 py-2 w-full"/>
                </div>
                <div>
                    <button type="submit" className="bg-blue-800 w-full py-3 rounded-md">
                        Save Changes
                    </button>
                </div>
                <h2>{message}</h2>
            </form>
        </div>
    )
}