import json
from typing import Dict, List, Optional
from pathlib import Path
import uuid

from core.models.bug import Bug, BugPriority, BugStatus


class BugManager:
    
    def __init__(self, project_data: Dict, version: str):
        self.project_data = project_data
        self.version = version
        
        self._ensure_version_structure()
        self.bugs: Dict[str, Bug] = self._load_bugs_from_data()
    
    def _ensure_version_structure(self):
        if "versions" not in self.project_data:
            self.project_data["versions"] = {}
        
        if self.version not in self.project_data["versions"]:
            self.project_data["versions"][self.version] = {
                "tasks": {},
                "bugs": {}
            }
        elif "bugs" not in self.project_data["versions"][self.version]:
            self.project_data["versions"][self.version]["bugs"] = {}
    
    def _load_bugs_from_data(self) -> Dict[str, Bug]:
        bugs_dict = {}
        
        try:
            version_data = self.project_data["versions"][self.version]
            bugs_data = version_data.get("bugs", {})
            
            for bug_id, bug_data in bugs_data.items():
                bug = Bug.from_dict(bug_data)
                bugs_dict[bug_id] = bug
            
            return bugs_dict
        except Exception as e:
            print(f"Error loading bugs: {e}")
            return {}
    
    def save_to_project_data(self):
        try:
            version_data = self.project_data["versions"][self.version]
            version_data["bugs"] = {
                bug_id: bug.to_dict() 
                for bug_id, bug in self.bugs.items()
            }
            return True
        except Exception as e:
            print(f"Error saving bugs to project data: {e}")
            return False
    
    @property
    def count(self) -> int:
        return len(self.bugs)
    
    @property
    def open_count(self) -> int:
        return sum(1 for bug in self.bugs.values() if bug.status == BugStatus.OPEN)
    
    @property
    def fixed_count(self) -> int:
        return sum(1 for bug in self.bugs.values() if bug.status == BugStatus.FIXED)
    
    @property
    def critical_count(self) -> int:
        return sum(1 for bug in self.bugs.values() if bug.priority == BugPriority.CRITICAL)
    
    def add_bug(self, 
                title: str,
                description: str = "",
                priority: BugPriority = BugPriority.MEDIUM,
                task_id: str = "",
                steps_to_reproduce: str = "",
                expected_result: str = "",
                actual_result: str = "",
                screenshot_path: str = "",
                author: str = "") -> Optional[Bug]:
        bug_id = f"BUG-{str(uuid.uuid4())[:8].upper()}"
        
        bug = Bug(
            id=bug_id,
            title=title,
            description=description,
            priority=priority,
            task_id=task_id,
            steps_to_reproduce=steps_to_reproduce,
            expected_result=expected_result,
            actual_result=actual_result,
            screenshot_path=screenshot_path,
            author=author
        )
        
        self.bugs[bug_id] = bug
        
        if self.save_to_project_data():
            return bug
        return None
    
    def get_bug(self, bug_id: str) -> Optional[Bug]:
        return self.bugs.get(bug_id)
    
    def get_all_bugs(self) -> List[Bug]:
        return list(self.bugs.values())
    
    def get_bugs_by_task(self, task_id: str) -> List[Bug]:
        return [bug for bug in self.bugs.values() if bug.task_id == task_id]
    
    def get_bugs_by_status(self, status: BugStatus) -> List[Bug]:
        return [bug for bug in self.bugs.values() if bug.status == status]
    
    def get_bugs_by_priority(self, priority: BugPriority) -> List[Bug]:
        return [bug for bug in self.bugs.values() if bug.priority == priority]
    
    def filter_bugs(self, 
               priority_filter: Optional[BugPriority] = None,
               status_filter: Optional[BugStatus] = None,
               task_id_filter: str = "",
               search_text: str = "") -> List[Bug]:
        filtered_bugs = self.get_all_bugs()
        
        if priority_filter:
            filtered_bugs = [b for b in filtered_bugs if b.priority == priority_filter]
        
        if status_filter:
            filtered_bugs = [b for b in filtered_bugs if b.status == status_filter]
        
        if task_id_filter:
            if task_id_filter.startswith("TASK-"):
                filtered_bugs = [b for b in filtered_bugs if b.task_id == task_id_filter]
            else:
                filtered_bugs = [b for b in filtered_bugs if task_id_filter.lower() in b.task_id.lower()]
        
        if search_text:
            search_lower = search_text.lower()
            filtered_bugs = [
                b for b in filtered_bugs
                if search_lower in b.title.lower() 
                or search_lower in b.description.lower()
                or search_lower in b.id.lower()
                or search_lower in b.task_id.lower()
            ]
        
        return filtered_bugs
    
    def update_bug(self, bug_id: str, **kwargs) -> bool:
        bug = self.get_bug(bug_id)
        if not bug:
            return False
        
        try:
            if 'title' in kwargs:
                bug._title = kwargs['title']
            if 'description' in kwargs:
                bug._description = kwargs['description']
            if 'priority' in kwargs and isinstance(kwargs['priority'], BugPriority):
                bug.update_priority(kwargs['priority'])
            if 'status' in kwargs and isinstance(kwargs['status'], BugStatus):
                bug.update_status(kwargs['status'])
            if 'task_id' in kwargs:
                bug.update_task_id(kwargs['task_id'])
            if 'steps_to_reproduce' in kwargs:
                bug._steps_to_reproduce = kwargs['steps_to_reproduce']
            if 'expected_result' in kwargs:
                bug._expected_result = kwargs['expected_result']
            if 'actual_result' in kwargs:
                bug._actual_result = kwargs['actual_result']
            if 'screenshot_path' in kwargs:
                bug._screenshot_path = kwargs['screenshot_path']
            if 'assigned_to' in kwargs:
                bug.assign_to(kwargs['assigned_to'])
            
            return self.save_to_project_data()
        except Exception as e:
            print(f"Error updating bug: {e}")
            return False
    
    def add_comment(self, bug_id: str, author: str, text: str) -> bool:
        bug = self.get_bug(bug_id)
        if not bug:
            return False
        
        bug.add_comment(author, text)
        return self.save_to_project_data()
    
    def delete_bug(self, bug_id: str) -> bool:
        if bug_id in self.bugs:
            del self.bugs[bug_id]
            return self.save_to_project_data()
        return False
    
    def get_bug_statistics(self) -> Dict:
        return {
            "total": self.count,
            "open": self.open_count,
            "fixed": self.fixed_count,
            "critical": self.critical_count,
            "by_priority": {
                priority.value: len(self.get_bugs_by_priority(priority))
                for priority in BugPriority
            },
            "by_status": {
                status.value: len(self.get_bugs_by_status(status))
                for status in BugStatus
            }
        }