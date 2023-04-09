


export default function FeedingSchedule({sched}) {
    return (
        <div className="bg-indigo-900/10 py-2 px-4 h-fit">
            <div className="text-left">
                <span className="text-gray-500">{"Time: "}</span> 
                <span className="text-lg text-blue-400 font-bold">{sched.time_scheduled}</span>
            </div>
            <div className="text-left">
                <span className="text-gray-500">{"Feed Amount: "}</span> 
                <span className="text-lg text-blue-400 font-bold">{sched.feed_amount}</span>
                <span className="text-blue-400">{" grams"}</span> 
            </div>
            <div className="text-left">
                <span className="text-gray-500">{"Status: "}</span> 
                <span className="text-lg text-blue-400 font-bold">{sched.done_for_the_day ? "Done" : "Upcoming"}</span>
            </div>
        </div>
    )
}