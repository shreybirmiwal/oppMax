import React, { useState } from "react";
import ActivityFeed from "./components/ActivityFeed";
import Analysis from "./components/Analysis";

function App() {
  const [activeTab, setActiveTab] = useState("feed");

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-md fixed bottom-0 inset-x-0 flex justify-around p-2">
        <button
          className={`w-full p-2 ${activeTab === "feed" ? "text-blue-500" : ""}`}
          onClick={() => setActiveTab("feed")}
        >
          Activity Feed
        </button>
        <button
          className={`w-full p-2 ${activeTab === "analysis" ? "text-blue-500" : ""}`}
          onClick={() => setActiveTab("analysis")}
        >
          Analysis
        </button>
      </nav>

      <div className="pt-4 pb-20">
        {activeTab === "feed" ? <ActivityFeed /> : <Analysis />}
      </div>
    </div>
  );
}

export default App;
