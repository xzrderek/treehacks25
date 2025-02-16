"use client";

import { useState, useEffect } from "react";
import { useRouter } from 'next/navigation';

interface Task {
  task_id: string;
  task_description: string;
  status: string;
  date: string;
  result?: string;
}

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState("");
  const [mounted, setMounted] = useState(false);
  const router = useRouter();

  const fetchTasks = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/tasks`);
      const data = await response.json();
      
      const updatedTasks = Object.values(data.tasks).map((task: any) => ({
        task_id: task.task_id,
        task_description: task.task_description,
        status: task.status.charAt(0).toUpperCase() + task.status.slice(1),
        date: task.date,
        result: task.result
      }));
      
      setTasks(updatedTasks);
    } catch (error) {
      console.error("Error fetching tasks:", error);
    }
  };

  useEffect(() => {
    setMounted(true);
    fetchTasks();
    const interval = setInterval(fetchTasks, 2000);
    return () => clearInterval(interval);
  }, []);

  if (!mounted) {
    return null;
  }

  const handleAddTask = async () => {
    if (!newTask.trim()) return;

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/tasks/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: newTask }),
      });

      if (!response.ok) throw new Error("Failed to add task");

      const newTaskData = await response.json();
      setTasks([...tasks, { 
        task_id: newTaskData.task_id, 
        task_description: newTask, 
        status: "Pending", 
        date: "2024-02-14 12:00:00",  // Fixed date for testing
      }]);
      setNewTask("");
    } catch (error) {
      console.error("Error adding task:", error);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/tasks/${taskId}`, {
        method: 'DELETE',
      });

      if (!response.ok) throw new Error('Failed to delete task');
      setTasks(tasks.filter(task => task.task_id !== taskId));
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "Completed": return "bg-green-200 text-green-700";
      case "Processing": return "bg-yellow-200 text-yellow-700";
      case "Failed": return "bg-red-200 text-red-700";
      default: return "bg-gray-200 text-gray-700";
    }
  };

  return (
    <div className="w-full max-w-7xl mx-auto p-6">
      {/* Header with Task Input */}
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Hello, I'm Meredith</h1>
        <div className="mt-6 flex gap-4">
          <div className="flex-1 flex gap-4">
            <input
              type="text"
              placeholder="What can I help you with? (e.g., 'Schedule a meeting with radiology')"
              value={newTask}
              onChange={(e) => setNewTask(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleAddTask();
                }
              }}
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={handleAddTask}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition font-medium"
            >
              Add Task
            </button>
          </div>
        </div>
      </header>

      {/* Task Queue */}
      <section>
        <h2 className="text-xl font-semibold mb-4">Task Queue</h2>
        <div className="space-y-4">
          {tasks.map((task) => (
            <div
              key={task.task_id}
              onClick={() => router.push(`/tasks/${task.task_id}`)}
              className="bg-white rounded-lg p-4 shadow-sm hover:shadow-md transition cursor-pointer border border-gray-100"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(task.status)}`}>
                      {task.status}
                    </span>
                  </div>
                  <p className="text-lg font-medium">{task.task_description}</p>
                  <p className="text-sm text-gray-500 mt-1">{task.date}</p>
                </div>
                <div className="flex items-center gap-4">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteTask(task.task_id);
                    }}
                    className="text-gray-400 hover:text-red-600 transition"
                  >
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          ))}
          
          {tasks.length === 0 && (
            <div className="text-center py-12">
              <svg
                className="mx-auto h-12 w-12 text-gray-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                />
              </svg>
              <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
              <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}