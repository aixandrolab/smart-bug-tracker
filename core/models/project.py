import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class Project:
    def __init__(self, name: str, description: str = "", author: str = "",
                 created_at: Optional[str] = None):
        self._name = name
        self._description = description
        self._author = author
        self._github_url: str = ""
        self._created_at = created_at or datetime.now().isoformat()
        self._versions: List[str] = []
        self._developers: List[str] = [author] if author else []
        self._testers: List[str] = []
        
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def author(self) -> str:
        return self._author
    
    @property
    def github_url(self) -> str:
        return self._github_url
    
    @property
    def created_at(self) -> str:
        return self._created_at
    
    @property
    def versions(self) -> List[str]:
        return self._versions
    
    @property
    def developers(self) -> List[str]:
        return self._developers
    
    @property
    def testers(self) -> List[str]:
        return self._testers

    @github_url.setter
    def github_url(self, url: str):
        self._github_url = url
    
    def add_version(self, version_name: str):
        if version_name not in self._versions:
            self._versions.append(version_name)
    
    def remove_version(self, version_name: str):
        if version_name in self._versions:
            self._versions.remove(version_name)
    
    def add_developer(self, developer: str):
        if developer not in self._developers:
            self._developers.append(developer)
    
    def add_tester(self, tester: str):
        if tester not in self._testers:
            self._testers.append(tester)
    
    def to_dict(self) -> Dict:
        return {
            "name": self._name,
            "description": self._description,
            "author": self._author,
            "created_at": self._created_at,
            "versions": self._versions,
            "developers": self._developers,
            "testers": self._testers,
            "github_url": self._github_url
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Project':
        project = Project(
            name=data['name'],
            description=data['description'],
            author=data['author'],
            created_at=data['created_at']
        )
        project._versions = data.get('versions', [])
        project._developers = data.get('developers', [])
        project._testers = data.get('testers', [])
        project._github_url = data.get('github_url', '')
        return project