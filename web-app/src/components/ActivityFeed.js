import React, { useEffect, useState } from "react";
import { db, collection, query, orderBy, onSnapshot } from "../firebase";

const ActivityFeed = () => {
    const [activities, setActivities] = useState([]);

    useEffect(() => {
        const q = query(collection(db, "data"), orderBy("timestamp", "desc"));
        const unsubscribe = onSnapshot(q, (snapshot) => {
            const activityData = snapshot.docs.map(doc => ({
                id: doc.id,
                ...doc.data(),
            }));
            setActivities(activityData);
        });
        return () => unsubscribe();
    }, []);

    return (
        <div className="p-4">
            <h2 className="text-lg font-semibold mb-4">Activity Feed</h2>
            {activities.map((activity) => (
                <div key={activity.id} className="bg-white rounded-lg shadow-md p-4 mb-4">
                    <img src={activity.img_url} alt={activity.activity} className="w-full h-40 object-cover rounded-md" />
                    <h2 className="text-lg font-semibold mt-2">{activity.activity}</h2>
                    <div className="mt-2">
                        <div className="flex items-center justify-between">
                            <span>Health Score:</span>
                            <input type="range" min="-10" max="10" value={activity.healthScore} readOnly className="slider w-1/2" />
                            <span>{activity.healthScore}</span>
                        </div>
                        <div className="flex items-center justify-between">
                            <span>Career Score:</span>
                            <input type="range" min="-10" max="10" value={activity.careerScore} readOnly className="slider w-1/2" />
                            <span>{activity.careerScore}</span>
                        </div>
                        <div className="flex items-center justify-between">
                            <span>Social Score:</span>
                            <input type="range" min="-10" max="10" value={activity.socialScore} readOnly className="slider w-1/2" />
                            <span>{activity.socialScore}</span>
                        </div>
                    </div>
                    <p className="mt-2 text-sm">Alternative Activity: {activity.alternateActivity}</p>
                </div>
            ))}
        </div>
    );
};

export default ActivityFeed;
