from datetime import datetime
import enum
import uuid

class TaskStatus(enum.Enum):
    QUEUED = 'QUEUED'          # Waiting to be processed
    IN_PROGRESS = 'IN_PROGRESS' # Currently being processed
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String, nullable=False, default=TaskStatus.QUEUED.value)
    priority = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    error = db.Column(db.Text)
    result = db.Column(db.Text)  # Store final result if any

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'error': self.error,
            'result': self.result
        }
