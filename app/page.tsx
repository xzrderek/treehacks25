"use client";

import { useState, useEffect } from "react";

interface Task {
  task_id: string;
  task_description: string;
  status: string;
  date: string;
}

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);

  useEffect(() => {
    // Simulating fetching tasks from an API
    setTasks([
      {
        task_id: "1",
        task_description: "Make Calendar Invite for David",
        status: "Complete",
        date: "2/13",
      },
      {
        task_id: "2",
        task_description: "Make Calendar Invite for Derek",
        status: "In Progress",
        date: "2/13",
      },
    ]);
  }, []);

  return (
    <main className="w-full max-w-3xl bg-white shadow-md rounded-2xl p-6">
      <h1 className="text-2xl font-semibold text-center mb-4">My Tasks</h1>

      {/* Header Row */}
      <div className="grid grid-cols-[2fr_1fr_1fr] font-medium text-gray-700 border-b pb-2">
        <div className="text-left">Task</div>
        <div className="pl-6">Status</div>
        <div className="text-right">Date</div>
      </div>

      {/* Task List */}
      <div className="mt-4 space-y-3">
        {tasks.map((task) => (
          <div
            key={task.task_id}
            className="grid grid-cols-[2fr_1fr_1fr] items-center bg-gray-50 px-4 py-3 rounded-lg shadow-sm"
          >
            <div className="text-left font-medium">{task.task_description}</div>
            <div
              className={`px-3 py-1 rounded-lg text-sm font-semibold ${
                task.status === "Complete"
                  ? "bg-green-200 text-green-700"
                  : "bg-yellow-200 text-yellow-700"
              } ml-6`}
            >
              {task.status}
            </div>
            <div className="text-right text-gray-500">{task.date}</div>
          </div>
        ))}
      </div>
    </main>
  );
}