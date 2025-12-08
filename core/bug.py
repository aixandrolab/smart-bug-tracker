import json
from datetime import datetime
from typing import Dict, Optional, List
from enum import Enum


class BugStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    FIXED = "fixed"
    WONT_FIX = "wont_fix"
    DUPLICATE = "duplicate"
    INVALID = "invalid"


class BugPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    
    @staticmethod
    def from_string(priority_str: str) -> 'BugPriority':
        for priority in BugPriority:
            if priority.value == priority_str.lower():
                return priority
        return BugPriority.MEDIUM


class Bug:    
    def __init__(self, 
                 id: str, 
                 title: str, 
                 description: str = "",
                 priority: BugPriority = BugPriority.MEDIUM,
                 status: BugStatus = BugStatus.OPEN,
                 created_at: Optional[str] = None,
                 task_id: str = "",
                 steps_to_reproduce: str = "",
                 expected_result: str = "",
                 actual_result: str = "",
                 screenshot_path: str = "",
                 author: str = "",
                 assigned_to: str = ""):
        
        self._id = id
        self._title = title
        self._description = description
        self._priority = priority
        self._status = status
        self._created_at = created_at or datetime.now().isoformat()
        self._task_id = task_id
        self._steps_to_reproduce = steps_to_reproduce
        self._expected_result = expected_result
        self._actual_result = actual_result
        self._screenshot_path = screenshot_path
        self._author = author
        self._assigned_to = assigned_to
        self._comments: List[Dict] = []
        
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
    def priority(self) -> BugPriority:
        return self._priority
    
    @property
    def status(self) -> BugStatus:
        return self._status
    
    @property
    def created_at(self) -> str:
        return self._created_at
    
    @property
    def task_id(self) -> str:
        return self._task_id
    
    @property
    def steps_to_reproduce(self) -> str:
        return self._steps_to_reproduce
    
    @property
    def expected_result(self) -> str:
        return self._expected_result
    
    @property
    def actual_result(self) -> str:
        return self._actual_result
    
    @property
    def screenshot_path(self) -> str:
        return self._screenshot_path
    
    @property
    def author(self) -> str:
        return self._author
    
    @property
    def assigned_to(self) -> str:
        return self._assigned_to
    
    @property
    def comments(self) -> List[Dict]:
        return self._comments
    
    def add_comment(self, author: str, text: str):
        comment = {
            "author": author,
            "text": text,
            "created_at": datetime.now().isoformat()
        }
        self._comments.append(comment)
    
    def update_status(self, status: BugStatus):
        self._status = status
    
    def update_priority(self, priority: BugPriority):
        self._priority = priority
    
    def assign_to(self, person: str):
        self._assigned_to = person
    
    def update_task_id(self, task_id: str):
        self._task_id = task_id
    
    def get_status_color(self):
        if self.status == BugStatus.FIXED:
            return "#4CAF50"
        elif self.status == BugStatus.OPEN:
            return "#F44336"
        elif self.status == BugStatus.IN_PROGRESS:
            return "#2196F3"
        elif self.status in [BugStatus.WONT_FIX, BugStatus.DUPLICATE, BugStatus.INVALID]:
            return "#9E9E9E"
        return "#FF9800"
    
    def to_dict(self) -> Dict:
        return {
            "id": self._id,
            "title": self._title,
            "description": self._description,
            "priority": self._priority.value,
            "status": self._status.value,
            "created_at": self._created_at,
            "task_id": self._task_id,
            "steps_to_reproduce": self._steps_to_reproduce,
            "expected_result": self._expected_result,
            "actual_result": self._actual_result,
            "screenshot_path": self._screenshot_path,
            "author": self._author,
            "assigned_to": self._assigned_to,
            "comments": self._comments
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Bug':
        bug = Bug(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            priority=BugPriority.from_string(data['priority']),
            status=BugStatus(data['status']),
            created_at=data['created_at'],
            task_id=data.get('task_id', ''),
            steps_to_reproduce=data.get('steps_to_reproduce', ''),
            expected_result=data.get('expected_result', ''),
            actual_result=data.get('actual_result', ''),
            screenshot_path=data.get('screenshot_path', ''),
            author=data.get('author', ''),
            assigned_to=data.get('assigned_to', '')
        )
        
        comments = data.get('comments', [])
        bug._comments = comments
        
        return bug