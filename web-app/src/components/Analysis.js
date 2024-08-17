import React, { useEffect, useState } from "react";
import { db, collection, query, onSnapshot } from "../firebase";

const Analysis = () => {
    const [analysis, setAnalysis] = useState({});

    useEffect(() => {
        const q = query(collection(db, "data"));
        const unsubscribe = onSnapshot(q, (snapshot) => {
            const activities = snapshot.docs.map(doc => doc.data());

            const worstActivities = activities.reduce((acc, activity) => {
                if (activity.healthScore < acc.healthScore) acc.health = activity;
                if (activity.careerScore < acc.careerScore) acc.career = activity;
                if (activity.socialScore < acc.socialScore) acc.social = activity;
                return acc;
            }, { health: {}, career: {}, social: {} });

            setAnalysis(worstActivities);
        });
        return () => unsubscribe();
    }, []);

    return (
        <div className="p-4">
            <h2 className="text-lg font-semibold mb-4">Analysis</h2>
            <div className="bg-white rounded-lg shadow-md p-4 mb-4">
                <h3 className="font-semibold">Health Impact</h3>
                <p>Worst Activity: {analysis.health?.activity}</p>
                <p>Alternative: {analysis.health?.alternateActivity}</p>
            </div>
            <div className="bg-white rounded-lg shadow-md p-4 mb-4">
                <h3 className="font-semibold">Career Impact</h3>
                <p>Worst Activity: {analysis.career?.activity}</p>
                <p>Alternative: {analysis.career?.alternateActivity}</p>
            </div>
            <div className="bg-white rounded-lg shadow-md p-4 mb-4">
                <h3 className="font-semibold">Social Impact</h3>
                <p>Worst Activity: {analysis.social?.activity}</p>
                <p>Alternative: {analysis.social?.alternateActivity}</p>
            </div>
        </div>
    );
};

export default Analysis;
