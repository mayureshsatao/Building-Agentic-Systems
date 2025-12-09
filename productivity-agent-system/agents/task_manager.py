"""
Task Manager Agent
Specializes in task creation, prioritization, and tracking
"""
from crewai import Agent
from typing import List
from crewai_tools import tool


def create_task_manager_agent(tools: List) -> Agent:
    """
    Create and configure the Task Manager Agent
    
    This agent is responsible for:
    - Creating and organizing tasks
    - Applying prioritization frameworks
    - Tracking task progress
    - Managing deadlines
    """
    
    return Agent(
        role="Task Management Specialist",
        goal="""Efficiently manage tasks by creating, organizing, and prioritizing them 
        based on urgency, importance, and user preferences. Ensure all tasks have clear 
        deadlines and actionable descriptions.""",
        backstory="""You are an expert in personal productivity and task management with 
        years of experience implementing GTD (Getting Things Done), Eisenhower Matrix, 
        and other proven prioritization frameworks. You excel at breaking down complex 
        projects into manageable tasks and ensuring nothing falls through the cracks. 
        
        You understand that effective task management requires:
        - Clear, actionable task descriptions
        - Realistic deadline estimation
        - Smart prioritization based on multiple factors
        - Regular review and adjustment of priorities
        
        You're skilled at identifying dependencies between tasks and can recommend the 
        optimal order for completing work.""",
        verbose=True,
        allow_delegation=False,
        tools=tools,
        memory=True
    )


@tool("Task Prioritization Framework")
def prioritize_tasks_tool(tasks_json: str) -> str:
    """
    Apply prioritization framework to a list of tasks
    
    Args:
        tasks_json: JSON string containing task list with urgency and importance scores
    
    Returns:
        JSON string with prioritized tasks and recommended order
    """
    import json
    
    try:
        tasks = json.loads(tasks_json)
        
        # Eisenhower Matrix prioritization
        for task in tasks:
            urgency = task.get('urgency', 5)  # 1-10 scale
            importance = task.get('importance', 5)  # 1-10 scale
            
            # Calculate priority score
            priority_score = (urgency * 0.4) + (importance * 0.6)
            
            # Assign quadrant
            if urgency > 6 and importance > 6:
                quadrant = "DO FIRST - Urgent & Important"
                priority_level = "critical"
            elif urgency <= 6 and importance > 6:
                quadrant = "SCHEDULE - Not Urgent but Important"
                priority_level = "high"
            elif urgency > 6 and importance <= 6:
                quadrant = "DELEGATE - Urgent but Not Important"
                priority_level = "medium"
            else:
                quadrant = "ELIMINATE - Neither Urgent nor Important"
                priority_level = "low"
            
            task['priority_score'] = round(priority_score, 2)
            task['quadrant'] = quadrant
            task['priority_level'] = priority_level
        
        # Sort by priority score
        tasks.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return json.dumps({
            "prioritized_tasks": tasks,
            "recommendation": "Focus on 'DO FIRST' tasks immediately, schedule time for 'SCHEDULE' tasks"
        }, indent=2)
    
    except Exception as e:
        return json.dumps({"error": str(e)})
