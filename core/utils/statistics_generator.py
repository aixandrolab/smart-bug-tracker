class StatisticsGenerator:
    
    @staticmethod
    def generate_project_stats(project, task_manager, bug_manager):
        if not task_manager or not bug_manager:
            return {}
        
        task_stats = task_manager.get_task_statistics()
        bug_stats = bug_manager.get_bug_statistics()
        
        stats = {
            "project_info": {
                "name": project.name,
                "author": project.author,
                "versions": len(project.versions),
                "github_url": project.github_url
            },
            "tasks": {
                "total": task_stats.get('total', 0),
                "by_priority": {
                    "critical": task_stats.get('critical', 0),
                    "high": task_stats.get('high', 0),
                    "medium": task_stats.get('medium', 0),
                    "low": task_stats.get('low', 0)
                },
                "by_status": task_stats.get('by_status', {}),
                "status_summary": {
                    "todo": task_stats.get('todo', 0),
                    "in_progress": task_stats.get('in_progress', 0),
                    "done": task_stats.get('done', 0)
                }
            },
            "bugs": {
                "total": bug_stats.get('total', 0),
                "open": bug_stats.get('open', 0),
                "fixed": bug_stats.get('fixed', 0),
                "by_priority": {
                    "critical": bug_stats.get('critical', 0),
                    "high": bug_stats.get('high', 0),
                    "medium": bug_stats.get('medium', 0),
                    "low": bug_stats.get('low', 0)
                },
                "by_status": bug_stats.get('by_status', {})
            },
            "progress": {
                "completion_rate": StatisticsGenerator._calculate_completion_rate(task_stats),
                "bug_resolution_rate": StatisticsGenerator._calculate_bug_resolution_rate(bug_stats),
                "task_bug_ratio": StatisticsGenerator._calculate_task_bug_ratio(task_stats, bug_stats)
            }
        }
        
        return stats
    
    @staticmethod
    def _calculate_completion_rate(task_stats):
        total = task_stats.get('total', 0)
        done = task_stats.get('done', 0)
        
        if total == 0:
            return 0
        return round((done / total) * 100, 1)
    
    @staticmethod
    def _calculate_bug_resolution_rate(bug_stats):
        total = bug_stats.get('total', 0)
        fixed = bug_stats.get('fixed', 0)
        
        if total == 0:
            return 0
        return round((fixed / total) * 100, 1)
    
    @staticmethod
    def _calculate_task_bug_ratio(task_stats, bug_stats):
        tasks = task_stats.get('total', 0)
        bugs = bug_stats.get('total', 0)
        
        if tasks == 0:
            return 0
        return round(bugs / tasks, 2)