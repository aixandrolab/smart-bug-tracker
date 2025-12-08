import json
import os
from typing import Dict, List, Optional
from pathlib import Path
import uuid

from core.task import Task, TaskPriority, TaskStatus


class TaskManager:
    
    def __init__(self, project_data: Dict, version: str):
        self.project_data = project_data
        self.version = version
        
        self._ensure_version_structure()
        self.tasks: Dict[str, Task] = self._load_tasks_from_data()
    
    def _ensure_version_structure(self):
        if "versions" not in self.project_data:
            self.project_data["versions"] = {}
        
        if self.version not in self.project_data["versions"]:
            self.project_data["versions"][self.version] = {
                "tasks": {},
                "bugs": {}
            }
        elif "tasks" not in self.project_data["versions"][self.version]:
            self.project_data["versions"][self.version]["tasks"] = {}
    
    def _load_tasks_from_data(self) -> Dict[str, Task]:
        tasks_dict = {}
        
        try:
            version_data = self.project_data["versions"][self.version]
            tasks_data = version_data.get("tasks", {})
            
            for task_id, task_data in tasks_data.items():
                task = Task.from_dict(task_data)
                tasks_dict[task_id] = task
            
            return tasks_dict
        except Exception as e:
            print(f"Error loading tasks: {e}")
            return {}
    
    def save_to_project_data(self):
        try:
            version_data = self.project_data["versions"][self.version]
            version_data["tasks"] = {
                task_id: task.to_dict() 
                for task_id, task in self.tasks.items()
            }
            return True
        except Exception as e:
            print(f"Error saving tasks to project data: {e}")
            return False
    
    @property
    def count(self) -> int:
        return len(self.tasks)
    
    @property
    def todo_count(self) -> int:
        return sum(1 for task in self.tasks.values() if task.status == TaskStatus.TODO)
    
    @property
    def in_progress_count(self) -> int:
        return sum(1 for task in self.tasks.values() if task.status == TaskStatus.IN_PROGRESS)
    
    @property
    def critical_count(self) -> int:
        return sum(1 for task in self.tasks.values() if task.priority == TaskPriority.CRITICAL)
    
    def add_task(self, 
                 title: str, 
                 description: str = "",
                 priority: TaskPriority = TaskPriority.MEDIUM,
                 test_instructions: str = "",
                 assigned_to: str = "") -> Optional[Task]:
        task_id = f"TASK-{str(uuid.uuid4())[:8].upper()}"
        
        task = Task(
            id=task_id,
            title=title,
            description=description,
            priority=priority,
            version=self.version,
            test_instructions=test_instructions,
            assigned_to=assigned_to
        )
        
        self.tasks[task_id] = task
        
        if self.save_to_project_data():
            return task
        return None
    
    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> List[Task]:
        return list(self.tasks.values())
    
    def get_tasks_by_priority(self, priority: TaskPriority) -> List[Task]:
        return [task for task in self.tasks.values() if task.priority == priority]
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        return [task for task in self.tasks.values() if task.status == status]
    
    def update_task(self, task_id: str, **kwargs) -> bool:
        task = self.get_task(task_id)
        if not task:
            return False
        
        try:
            if 'title' in kwargs:
                task._title = kwargs['title']
            if 'description' in kwargs:
                task._description = kwargs['description']
            if 'test_description' in kwargs:
                task._description = kwargs['test_description']
            if 'priority' in kwargs and isinstance(kwargs['priority'], TaskPriority):
                task.update_priority(kwargs['priority'])
            if 'status' in kwargs and isinstance(kwargs['status'], TaskStatus):
                task.update_status(kwargs['status'])
            if 'test_instructions' in kwargs:
                task.update_test_instructions(kwargs['test_instructions'])
            if 'assigned_to' in kwargs:
                task.update_assigned_to(kwargs['assigned_to'])
            
            return self.save_to_project_data()
        except Exception as e:
            print(f"Error updating task: {e}")
            return False
    
    def delete_task(self, task_id: str) -> bool:
        if task_id in self.tasks:
            del self.tasks[task_id]
            return self.save_to_project_data()
        return False
    
    def get_task_statistics(self) -> Dict:
        return {
            "total": self.count,
            "todo": self.todo_count,
            "in_progress": self.in_progress_count,
            "critical": self.critical_count,
            "by_priority": {
                priority.value: len(self.get_tasks_by_priority(priority))
                for priority in TaskPriority
            },
            "by_status": {
                status.value: len(self.get_tasks_by_status(status))
                for status in TaskStatus
            }
        }

    def filter_tasks(self, 
                 priority_filter: Optional[TaskPriority] = None,
                 status_filter: Optional[TaskStatus] = None,
                 search_text: str = "") -> List[Task]:
        filtered_tasks = self.get_all_tasks()
        
        if priority_filter:
            filtered_tasks = [t for t in filtered_tasks if t.priority == priority_filter]
        
        if status_filter:
            filtered_tasks = [t for t in filtered_tasks if t.status == status_filter]
        
        if search_text:
            search_lower = search_text.lower()
            filtered_tasks = [
                t for t in filtered_tasks
                if search_lower in t.title.lower() 
                or search_lower in t.description.lower()
                or search_lower in t.id.lower()
            ]
        
        return filtered_tasks

    def get_tasks_by_priority(self, priority: TaskPriority) -> List[Task]:
        return self.filter_tasks(priority_filter=priority)