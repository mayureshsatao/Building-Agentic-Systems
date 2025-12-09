"""
Main Application - Personal Productivity Agentic System
"""
import os
from datetime import datetime
from crewai import Crew, Task, Process
from crewai_tools import SerperDevTool

# Import custom tools
from tools.workflow_optimizer import WorkflowOptimizerTool
from tools.date_calculator import DateCalculatorTool
from tools.file_processor import FileProcessorTool

# Import agent creators
from agents.controller import create_controller_agent
from agents.task_manager import create_task_manager_agent, prioritize_tasks_tool
from agents.schedule_optimizer import create_schedule_optimizer_agent
from agents.information_curator import create_information_curator_agent

# Import configuration
import config


class ProductivitySystem:
    """
    Main Productivity Agentic System
    Orchestrates multiple agents to manage tasks, schedules, and information
    """
    
    def __init__(self):
        """Initialize the productivity system with all agents and tools"""
        self._setup_environment()
        self._initialize_tools()
        self._initialize_agents()
    
    def _setup_environment(self):
        """Set up environment variables"""
        if not config.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY not found. Please set it in your .env file or environment"
            )
        os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY
    
    def _initialize_tools(self):
        """Initialize all tools"""
        print("Initializing tools...")
        
        # Custom tools
        self.workflow_optimizer = WorkflowOptimizerTool()
        self.date_calculator = DateCalculatorTool()
        self.file_processor = FileProcessorTool()
        
        # Built-in tools
        # Note: SerperDevTool requires SERPER_API_KEY for web search
        # For demo purposes, we'll include it but it's optional
        try:
            self.web_search = SerperDevTool()
        except:
            print("Web search not available (SERPER_API_KEY not set)")
            self.web_search = None
        
        # Organize tools by agent
        self.common_tools = [
            self.file_processor,
            self.date_calculator
        ]
        
        self.task_manager_tools = self.common_tools + [prioritize_tasks_tool]
        
        self.schedule_optimizer_tools = self.common_tools + [
            self.date_calculator
        ]
        
        self.information_curator_tools = self.common_tools.copy()
        if self.web_search:
            self.information_curator_tools.append(self.web_search)
        
        self.controller_tools = [
            self.workflow_optimizer,
            self.date_calculator,
            self.file_processor
        ]
        
        print("Tools initialized successfully")
    
    def _initialize_agents(self):
        """Initialize all agents"""
        print("Initializing agents...")
        
        self.task_manager = create_task_manager_agent(self.task_manager_tools)
        self.schedule_optimizer = create_schedule_optimizer_agent(self.schedule_optimizer_tools)
        self.information_curator = create_information_curator_agent(self.information_curator_tools)
        self.controller = create_controller_agent(self.controller_tools)
        
        print("Agents initialized successfully")
    
    def create_task(self, title: str, description: str = "", priority: str = "medium", 
                   deadline: str = "", estimated_duration: int = 60, tags: list = None):
        """
        Create a new task
        
        Args:
            title: Task title
            description: Detailed description
            priority: Priority level (low, medium, high, critical)
            deadline: Due date (ISO format)
            estimated_duration: Estimated time in minutes
            tags: List of tags for categorization
        """
        task = Task(
            description=f"""Create a new task with the following details:
            Title: {title}
            Description: {description}
            Priority: {priority}
            Deadline: {deadline}
            Estimated Duration: {estimated_duration} minutes
            Tags: {tags or []}
            
            Use the File Processor tool to save this task and confirm it was created successfully.
            """,
            agent=self.task_manager,
            expected_output="Confirmation that the task was created with task ID and details"
        )
        
        crew = Crew(
            agents=[self.task_manager],
            tasks=[task],
            process=Process.sequential,
            verbose=config.VERBOSE
        )
        
        result = crew.kickoff()
        return result
    
    def prioritize_my_tasks(self):
        """Analyze and prioritize all pending tasks"""
        task = Task(
            description="""Load all pending tasks from the file system and apply 
            prioritization frameworks to determine which tasks should be done first.
            
            Steps:
            1. Load all tasks with status 'pending' using the File Processor
            2. Apply the Eisenhower Matrix prioritization
            3. Provide a ranked list with recommendations
            4. Suggest which tasks to focus on today
            """,
            agent=self.task_manager,
            expected_output="Prioritized task list with clear recommendations for what to work on first"
        )
        
        crew = Crew(
            agents=[self.task_manager],
            tasks=[task],
            process=Process.sequential,
            verbose=config.VERBOSE
        )
        
        result = crew.kickoff()
        return result
    
    def optimize_my_schedule(self, date: str = None, tasks: list = None):
        """
        Optimize schedule for a given day
        
        Args:
            date: Date to optimize (ISO format, defaults to today)
            tasks: List of tasks to schedule
        """
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        task = Task(
            description=f"""Optimize the schedule for {date}.
            
            Steps:
            1. Load pending tasks from the file system
            2. Use the Date Calculator to find available time slots
            3. Analyze task priorities and estimated durations
            4. Create an optimized schedule that:
               - Puts high-priority tasks in peak productivity hours
               - Groups similar tasks together
               - Includes appropriate breaks
               - Prevents overload
            
            Provide a detailed schedule with specific time blocks for each task.
            """,
            agent=self.schedule_optimizer,
            expected_output="Optimized daily schedule with time blocks and recommendations"
        )
        
        crew = Crew(
            agents=[self.schedule_optimizer],
            tasks=[task],
            process=Process.sequential,
            verbose=config.VERBOSE
        )
        
        result = crew.kickoff()
        return result
    
    def get_workflow_insights(self, user_id: str = "default", time_range: str = "week"):
        """
        Get personalized workflow optimization insights
        
        Args:
            user_id: User identifier
            time_range: Analysis period (day, week, month)
        """
        task = Task(
            description=f"""Analyze workflow patterns and provide personalized 
            productivity recommendations for user {user_id} over the past {time_range}.
            
            Steps:
            1. Use the Workflow Optimizer tool to analyze patterns
            2. Generate personalized recommendations
            3. Identify productivity trends and areas for improvement
            4. Provide actionable advice
            
            Focus on being specific and actionable in your recommendations.
            """,
            agent=self.controller,
            expected_output="Detailed workflow analysis with personalized recommendations"
        )
        
        crew = Crew(
            agents=[self.controller],
            tasks=[task],
            process=Process.sequential,
            verbose=config.VERBOSE
        )
        
        result = crew.kickoff()
        return result
    
    def plan_my_day(self, focus_areas: list = None):
        """
        Complete daily planning - tasks, schedule, and insights
        
        Args:
            focus_areas: Optional list of areas to focus on today
        """
        # Task 1: Load and prioritize tasks
        task1 = Task(
            description="""Load all pending tasks and prioritize them for today.
            Apply smart prioritization considering urgency, importance, and deadlines.
            Identify the top 3-5 most important tasks for today.""",
            agent=self.task_manager,
            expected_output="Prioritized list of tasks for today with top priorities highlighted"
        )
        
        # Task 2: Optimize schedule
        task2 = Task(
            description="""Based on the prioritized tasks, create an optimized schedule 
            for today. Consider:
            - Peak productivity hours
            - Task dependencies
            - Energy levels throughout the day
            - Need for breaks
            
            Provide a time-blocked schedule.""",
            agent=self.schedule_optimizer,
            expected_output="Time-blocked schedule for today",
            context=[task1]
        )
        
        # Task 3: Get workflow insights
        task3 = Task(
            description="""Provide workflow optimization insights based on recent 
            productivity patterns. Suggest specific improvements for today's work.""",
            agent=self.controller,
            expected_output="Workflow insights and recommendations for today"
        )
        
        # Create crew with all agents
        crew = Crew(
            agents=[self.controller, self.task_manager, self.schedule_optimizer],
            tasks=[task1, task2, task3],
            process=Process.sequential,
            verbose=config.VERBOSE
        )
        
        result = crew.kickoff()
        return result
    
    def process_natural_language_request(self, request: str):
        """
        Process any natural language productivity request
        
        Args:
            request: User's request in natural language
        """
        task = Task(
            description=f"""Process this user request: "{request}"
            
            Analyze what the user needs and coordinate with appropriate specialized 
            agents to fulfill the request. You may need to:
            - Create or update tasks
            - Optimize schedules
            - Provide workflow insights
            - Search for information
            - Generate reports
            
            Delegate to specialized agents as needed and provide a comprehensive response.
            """,
            agent=self.controller,
            expected_output="Complete response addressing the user's request"
        )
        
        crew = Crew(
            agents=[
                self.controller,
                self.task_manager,
                self.schedule_optimizer,
                self.information_curator
            ],
            tasks=[task],
            process=Process.sequential,
            verbose=config.VERBOSE
        )
        
        result = crew.kickoff()
        return result


def main():
    """Main function for testing the system"""
    print("=" * 60)
    print("Personal Productivity Agentic System")
    print("=" * 60)
    print()
    
    # Initialize system
    system = ProductivitySystem()
    
    # Example usage
    print("\n--- Creating a new task ---")
    result = system.create_task(
        title="Complete project proposal",
        description="Write and submit the Q4 project proposal for review",
        priority="high",
        deadline="2024-12-01",
        estimated_duration=120,
        tags=["work", "urgent"]
    )
    print(result)
    
    print("\n--- Planning the day ---")
    result = system.plan_my_day()
    print(result)
    
    print("\n--- Getting workflow insights ---")
    result = system.get_workflow_insights()
    print(result)


if __name__ == "__main__":
    main()
