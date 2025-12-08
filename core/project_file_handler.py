import json
from pathlib import Path
from typing import Optional
from core.project import Project


class ProjectFileHandler:
    
    @staticmethod
    def save_project(project: Project, filepath: str) -> bool:
        try:
            filepath = Path(filepath)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            data = project.to_dict()
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error project saving: {e}")
            return False
    
    @staticmethod
    def load_project(filepath: str) -> Optional[Project]:
        try:
            filepath = Path(filepath)
            if not filepath.exists():
                return None
                
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return Project.from_dict(data)
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    @staticmethod
    def is_valid_project_file(filepath: str) -> bool:
        try:
            project = ProjectFileHandler.load_project(filepath)
            return project is not None
        except:
            return False