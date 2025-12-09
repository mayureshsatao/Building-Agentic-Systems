"""
File Processor Tool
Handles reading, writing, and processing task data files
"""
import json
import os
from typing import Dict, List, Any
from datetime import datetime

from crewai_tools import BaseTool


class FileProcessorTool(BaseTool):
    name: str = "File Processor"
    description: str = """
    Manages task data persistence including:
    - Load tasks from JSON file
    - Save tasks to JSON file
    - Update task status
    - Generate task reports
    - Export tasks in various formats
    
    Input should be a JSON string with:
    - action: 'load', 'save', 'update', 'delete', 'report', or 'export'
    - Additional parameters based on action
    """
    
    def __init__(self):
        super().__init__()
        self.tasks_file = "data/tasks.json"
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Ensure the data directory and file exist"""
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'w') as f:
                json.dump({"tasks": [], "last_updated": datetime.now().isoformat()}, f)
    
    def _run(self, input_str: str) -> str:
        """Execute file operations"""
        try:
            params = json.loads(input_str)
            action = params.get('action', '')
            
            if action == 'load':
                return self._load_tasks(params)
            elif action == 'save':
                return self._save_task(params)
            elif action == 'update':
                return self._update_task(params)
            elif action == 'delete':
                return self._delete_task(params)
            elif action == 'report':
                return self._generate_report(params)
            elif action == 'export':
                return self._export_tasks(params)
            else:
                return json.dumps({"error": "Invalid action"})
        
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON input"})
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def _load_tasks(self, params: Dict) -> str:
        """Load all tasks or filter by criteria"""
        try:
            with open(self.tasks_file, 'r') as f:
                data = json.load(f)
            
            tasks = data.get('tasks', [])
            
            # Apply filters
            status_filter = params.get('status')
            priority_filter = params.get('priority')
            
            if status_filter:
                tasks = [t for t in tasks if t.get('status') == status_filter]
            
            if priority_filter:
                tasks = [t for t in tasks if t.get('priority') == priority_filter]
            
            return json.dumps({
                "tasks": tasks,
                "count": len(tasks),
                "last_updated": data.get('last_updated', '')
            }, indent=2)
        
        except FileNotFoundError:
            return json.dumps({"tasks": [], "count": 0})
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def _save_task(self, params: Dict) -> str:
        """Save a new task"""
        try:
            with open(self.tasks_file, 'r') as f:
                data = json.load(f)
        except:
            data = {"tasks": [], "last_updated": ""}
        
        tasks = data.get('tasks', [])
        
        # Generate task ID
        task_id = f"task_{len(tasks) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        new_task = {
            "id": task_id,
            "title": params.get('title', 'Untitled Task'),
            "description": params.get('description', ''),
            "priority": params.get('priority', 'medium'),
            "status": params.get('status', 'pending'),
            "deadline": params.get('deadline', ''),
            "estimated_duration": params.get('estimated_duration', 60),
            "tags": params.get('tags', []),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        tasks.append(new_task)
        
        data['tasks'] = tasks
        data['last_updated'] = datetime.now().isoformat()
        
        with open(self.tasks_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return json.dumps({
            "status": "success",
            "message": "Task saved successfully",
            "task": new_task
        }, indent=2)
    
    def _update_task(self, params: Dict) -> str:
        """Update an existing task"""
        task_id = params.get('task_id')
        
        if not task_id:
            return json.dumps({"error": "task_id is required"})
        
        try:
            with open(self.tasks_file, 'r') as f:
                data = json.load(f)
        except:
            return json.dumps({"error": "No tasks file found"})
        
        tasks = data.get('tasks', [])
        task_found = False
        
        for task in tasks:
            if task['id'] == task_id:
                # Update fields
                if 'title' in params:
                    task['title'] = params['title']
                if 'description' in params:
                    task['description'] = params['description']
                if 'priority' in params:
                    task['priority'] = params['priority']
                if 'status' in params:
                    task['status'] = params['status']
                if 'deadline' in params:
                    task['deadline'] = params['deadline']
                if 'estimated_duration' in params:
                    task['estimated_duration'] = params['estimated_duration']
                
                task['updated_at'] = datetime.now().isoformat()
                task_found = True
                
                # Save updated data
                data['last_updated'] = datetime.now().isoformat()
                with open(self.tasks_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                return json.dumps({
                    "status": "success",
                    "message": "Task updated successfully",
                    "task": task
                }, indent=2)
        
        if not task_found:
            return json.dumps({"error": f"Task with id {task_id} not found"})
    
    def _delete_task(self, params: Dict) -> str:
        """Delete a task"""
        task_id = params.get('task_id')
        
        if not task_id:
            return json.dumps({"error": "task_id is required"})
        
        try:
            with open(self.tasks_file, 'r') as f:
                data = json.load(f)
        except:
            return json.dumps({"error": "No tasks file found"})
        
        tasks = data.get('tasks', [])
        original_count = len(tasks)
        
        tasks = [t for t in tasks if t['id'] != task_id]
        
        if len(tasks) == original_count:
            return json.dumps({"error": f"Task with id {task_id} not found"})
        
        data['tasks'] = tasks
        data['last_updated'] = datetime.now().isoformat()
        
        with open(self.tasks_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return json.dumps({
            "status": "success",
            "message": f"Task {task_id} deleted successfully",
            "remaining_tasks": len(tasks)
        })
    
    def _generate_report(self, params: Dict) -> str:
        """Generate a task report"""
        try:
            with open(self.tasks_file, 'r') as f:
                data = json.load(f)
        except:
            return json.dumps({"error": "No tasks file found"})
        
        tasks = data.get('tasks', [])
        
        if not tasks:
            return json.dumps({
                "report": "No tasks found",
                "summary": {"total": 0}
            })
        
        # Calculate statistics
        total = len(tasks)
        by_status = {}
        by_priority = {}
        overdue = 0
        
        now = datetime.now()
        
        for task in tasks:
            # Count by status
            status = task.get('status', 'pending')
            by_status[status] = by_status.get(status, 0) + 1
            
            # Count by priority
            priority = task.get('priority', 'medium')
            by_priority[priority] = by_priority.get(priority, 0) + 1
            
            # Check for overdue
            deadline = task.get('deadline', '')
            if deadline:
                try:
                    deadline_dt = datetime.fromisoformat(deadline)
                    if deadline_dt < now and task.get('status') != 'completed':
                        overdue += 1
                except:
                    pass
        
        report = {
            "summary": {
                "total_tasks": total,
                "by_status": by_status,
                "by_priority": by_priority,
                "overdue_tasks": overdue
            },
            "completion_rate": round(by_status.get('completed', 0) / total * 100, 1) if total > 0 else 0,
            "generated_at": datetime.now().isoformat()
        }
        
        return json.dumps(report, indent=2)
    
    def _export_tasks(self, params: Dict) -> str:
        """Export tasks in specified format"""
        format_type = params.get('format', 'json')
        
        try:
            with open(self.tasks_file, 'r') as f:
                data = json.load(f)
        except:
            return json.dumps({"error": "No tasks file found"})
        
        tasks = data.get('tasks', [])
        
        if format_type == 'csv':
            # Simple CSV export
            csv_lines = ["ID,Title,Priority,Status,Deadline"]
            for task in tasks:
                csv_lines.append(
                    f"{task['id']},{task['title']},{task['priority']},{task['status']},{task.get('deadline', '')}"
                )
            export_data = "\n".join(csv_lines)
            
            return json.dumps({
                "format": "csv",
                "data": export_data,
                "count": len(tasks)
            })
        else:
            # JSON export (default)
            return json.dumps({
                "format": "json",
                "data": tasks,
                "count": len(tasks)
            }, indent=2)
