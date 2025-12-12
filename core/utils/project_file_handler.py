import json
from pathlib import Path
from typing import Optional, Dict

from core.models.project import Project


class ProjectFileHandler:
    
    @staticmethod
    def save_project(project: Project, filepath: str, versions_data: Dict = None) -> bool:
        try:
            filepath = Path(filepath)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            project_data = {
                "meta": project.to_dict(),
                "versions": versions_data if versions_data else {}
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving project: {e}")
            return False
    
    @staticmethod
    def load_project(filepath: str) -> Optional[Project]:
        try:
            filepath = Path(filepath)
            if not filepath.exists():
                return None
                
            with open(filepath, 'r', encoding='utf-8') as f:
                project_data = json.load(f)
                
            meta_data = project_data.get("meta", {})

            if 'github_url' not in meta_data:
                meta_data['github_url'] = ''
            
            return Project.from_dict(meta_data)
        except Exception as e:
            print(f"Error loading project: {e}")
            return None
    
    @staticmethod
    def load_project_full(filepath: str) -> Optional[Dict]:
        try:
            filepath = Path(filepath)
            if not filepath.exists():
                return None
                
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading full project: {e}")
            return None
    
    @staticmethod
    def is_valid_project_file(filepath: str) -> bool:
        try:
            data = ProjectFileHandler.load_project_full(filepath)
            if not data:
                return False
            
            return "meta" in data and "versions" in data
        except:
            return False