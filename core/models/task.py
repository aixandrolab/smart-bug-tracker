import json
from datetime import datetime
from typing import Dict, Optional, List
from enum import Enum

from PyQt5.QtGui import QColor


class TaskPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high" 
    MEDIUM = "medium"
    LOW = "low"
    
    @staticmethod
    def from_string(priority_str: str) -> 'TaskPriority':
        for priority in TaskPriority:
            if priority.value == priority_str.lower():
                return priority
        return TaskPriority.MEDIUM


class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    READY_FOR_TEST = "ready_for_test"
    TESTING = "testing"
    DONE = "done"
    BLOCKED = "blocked"


class Task:
    
    def __init__(self, 
                 id: str, 
                 title: str, 
                 description: str = "",
                 priority: TaskPriority = TaskPriority.MEDIUM,
                 status: TaskStatus = TaskStatus.TODO,
                 created_at: Optional[str] = None,
                 version: str = "",
                 test_instructions: str = "",
                 assigned_to: str = ""):
        
        self._id = id
        self._title = title
        self._description = description
        self._priority = priority
        self._status = status
        self._created_at = created_at or datetime.now().isoformat()
        self._version = version
        self._test_instructions = test_instructions
        self._assigned_to = assigned_to
        self._bug_ids: List[str] = []
        
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def priority(self) -> TaskPriority:
        return self._priority
    
    @property
    def status(self) -> TaskStatus:
        return self._status
    
    @property
    def created_at(self) -> str:
        return self._created_at
    
    @property
    def version(self) -> str:
        return self._version
    
    @property
    def test_instructions(self) -> str:
        return self._test_instructions
    
    @property
    def assigned_to(self) -> str:
        return self._assigned_to
    
    @property
    def bug_ids(self) -> List[str]:
        return self._bug_ids

    def get_status_color(self) -> QColor:
        if self.status == TaskStatus.DONE:
            return QColor(100, 200, 100)
        elif self.status == TaskStatus.IN_PROGRESS:
            return QColor(100, 150, 255)
        elif self.status == TaskStatus.TESTING:
            return QColor(200, 150, 255)
        elif self.status == TaskStatus.READY_FOR_TEST:
            return QColor(255, 200, 100)
        elif self.status == TaskStatus.BLOCKED:
            return QColor(255, 100, 100)
        else:
            return QColor(200, 200, 200)
    
    def add_bug(self, bug_id: str):
        if bug_id not in self._bug_ids:
            self._bug_ids.append(bug_id)
    
    def remove_bug(self, bug_id: str):
        if bug_id in self._bug_ids:
            self._bug_ids.remove(bug_id)
    
    def update_description(self, description: str):
        self._description = description
    
    def update_priority(self, priority: TaskPriority):
        self._priority = priority
    
    def update_status(self, status: TaskStatus):
        self._status = status
    
    def update_test_instructions(self, instructions: str):
        self._test_instructions = instructions
    
    def update_assigned_to(self, person: str):
        self._assigned_to = person
    
    def to_dict(self) -> Dict:
        return {
            "id": self._id,
            "title": self._title,
            "description": self._description,
            "priority": self._priority.value,
            "status": self._status.value,
            "created_at": self._created_at,
            "version": self._version,
            "test_instructions": self._test_instructions,
            "assigned_to": self._assigned_to,
            "bug_ids": self._bug_ids
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Task':
        task = Task(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            priority=TaskPriority.from_string(data['priority']),
            status=TaskStatus(data['status']),
            created_at=data['created_at'],
            version=data.get('version', ''),
            test_instructions=data.get('test_instructions', ''),
            assigned_to=data.get('assigned_to', '')
        )
        
        bug_ids = data.get('bug_ids', [])
        for bug_id in bug_ids:
            task.add_bug(bug_id)
        
        return task