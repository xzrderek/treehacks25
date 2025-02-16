'use client';
import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { AlertCircle, CheckCircle, Clock } from 'lucide-react';

interface TaskMetadata {
  agent_version: string;
  priority: string;
  retries: number;
}

interface AgentLog {
  agent_scratchpad: string;
  planner_response: string;
  task_log: string;
}

interface Thought {
  step: number;
  thought: string;
  timestamp: string;
}

interface TaskDetails {
  task_id: string;
  task_description: string;
  status: string;
  date: string;
  started_at: string;
  completed_at: string;
  result?: string;
  thoughts?: Thought[];
  error_message?: string;
  agent_log?: AgentLog;
  metadata: TaskMetadata;
}

const AgentLogSection = ({ log }: { log: AgentLog }) => {
  return (
    <div className="space-y-6 mt-6">
      <div className="border rounded-lg p-4">
        <h3 className="text-lg font-semibold mb-3">Agent Scratchpad</h3>
        <div className="bg-gray-50 p-3 rounded whitespace-pre-wrap font-mono text-sm">
          {log.agent_scratchpad.split('\n').map((line, idx) => (
            <div key={idx} className="py-1">
              {line}
            </div>
          ))}
        </div>
      </div>

      <div className="border rounded-lg p-4">
        <h3 className="text-lg font-semibold mb-3">Planner Response</h3>
        <div className="space-y-2">
          {log.planner_response.split('\n').map((step, idx) => (
            <div key={idx} className="flex items-start gap-2 bg-gray-50 p-2 rounded">
              <div className="bg-blue-100 text-blue-800 rounded-full w-6 h-6 flex items-center justify-center flex-shrink-0">
                {idx + 1}
              </div>
              <div className="font-mono text-sm">{step}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="border rounded-lg p-4">
        <h3 className="text-lg font-semibold mb-3">Task Log</h3>
        <div className="space-y-2">
          {log.task_log.split('\n').map((entry, idx) => (
            <div key={idx} className="flex items-center gap-2 bg-gray-50 p-2 rounded">
              <Clock className="w-4 h-4 text-gray-500" />
              <span className="font-mono text-sm">{entry}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const StatusBadge = ({ status }: { status: string }) => {
  const getStatusColor = () => {
    switch (status.toLowerCase()) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      case 'running':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = () => {
    switch (status.toLowerCase()) {
      case 'completed':
        return <CheckCircle className="w-4 h-4" />;
      case 'failed':
        return <AlertCircle className="w-4 h-4" />;
      case 'running':
        return <Clock className="w-4 h-4" />;
      default:
        return null;
    }
  };

  return (
    <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium ${getStatusColor()}`}>
      {getStatusIcon()}
      {status}
    </span>
  );
};

export default function TaskPage() {
  const params = useParams();
  const taskId = params.taskId as string;
  const [task, setTask] = useState<TaskDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTaskDetails = async () => {
      if (!taskId) return;
      
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/tasks/${taskId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch task details');
        }
        const data = await response.json();
        setTask(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch task details');
      } finally {
        setLoading(false);
      }
    };
    fetchTaskDetails();
  }, [taskId]);

  if (loading) {
    return <div className="p-6">Loading...</div>;
  }

  if (error) {
    return <div className="p-6 text-red-600">Error: {error}</div>;
  }

  if (!task) {
    return <div className="p-6">Task not found</div>;
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Task Details</h1>
        <StatusBadge status={task.status} />
      </div>

      <div className="bg-white rounded-lg p-6 shadow-sm space-y-6">
        <div>
          <h2 className="text-lg font-semibold mb-2">Description</h2>
          <p>{task.task_description}</p>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <h2 className="text-lg font-semibold mb-2">Timing</h2>
            <div className="space-y-2 text-sm">
              <div>Started: {new Date(task.started_at).toLocaleString()}</div>
              <div>Completed: {new Date(task.completed_at).toLocaleString()}</div>
            </div>
          </div>

          <div>
            <h2 className="text-lg font-semibold mb-2">Metadata</h2>
            <div className="space-y-2 text-sm">
              <div>Agent Version: {task.metadata.agent_version}</div>
              <div>Priority: {task.metadata.priority}</div>
              <div>Retries: {task.metadata.retries}</div>
            </div>
          </div>
        </div>

        {task.result && (
          <div>
            <h2 className="text-lg font-semibold mb-2">Result</h2>
            <p>{task.result}</p>
          </div>
        )}

        {task.error_message && (
          <div>
            <h2 className="text-lg font-semibold text-red-600 mb-2">Error</h2>
            <p className="text-red-600">{task.error_message}</p>
          </div>
        )}

        {task.thoughts && task.thoughts.length > 0 && (
          <div>
            <h2 className="text-lg font-semibold mb-3">Progress Log</h2>
            <div className="space-y-2">
              {task.thoughts.map((thought, index) => (
                <div key={index} className="p-3 bg-gray-50 rounded">
                  <div className="flex items-center gap-2">
                    <div className="bg-blue-100 text-blue-800 rounded-full w-6 h-6 flex items-center justify-center">
                      {thought.step}
                    </div>
                    <span>{thought.thought}</span>
                  </div>
                  <div className="text-sm text-gray-500 mt-1">
                    {new Date(thought.timestamp).toLocaleString()}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {task.agent_log && (
          <div>
            <h2 className="text-lg font-semibold">Agent Log</h2>
            <AgentLogSection log={task.agent_log} />
          </div>
        )}
      </div>
    </div>
  );
}