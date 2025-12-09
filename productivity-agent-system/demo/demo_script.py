"""
Demo Script for Video Presentation
Demonstrates key features of the Personal Productivity Agentic System
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import ProductivitySystem
from datetime import datetime, timedelta
import json


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_task_creation():
    """Demo: Creating and managing tasks"""
    print_section("DEMO 1: Task Creation and Management")
    
    system = ProductivitySystem()
    
    print("Creating multiple tasks...")
    
    # Task 1
    system.create_task(
        title="Review budget proposal",
        description="Review Q4 budget and provide feedback",
        priority="high",
        deadline=(datetime.now() + timedelta(days=2)).isoformat(),
        estimated_duration=90,
        tags=["finance", "review"]
    )
    
    # Task 2
    system.create_task(
        title="Update project documentation",
        description="Add new features to project docs",
        priority="medium",
        deadline=(datetime.now() + timedelta(days=5)).isoformat(),
        estimated_duration=60,
        tags=["documentation", "project"]
    )
    
    # Task 3
    system.create_task(
        title="Team meeting preparation",
        description="Prepare slides and agenda for weekly team meeting",
        priority="high",
        deadline=(datetime.now() + timedelta(days=1)).isoformat(),
        estimated_duration=45,
        tags=["meeting", "team"]
    )
    
    print("\n✓ Tasks created successfully!")


def demo_prioritization():
    """Demo: Task prioritization"""
    print_section("DEMO 2: Intelligent Task Prioritization")
    
    system = ProductivitySystem()
    
    print("Analyzing and prioritizing all tasks...")
    result = system.prioritize_my_tasks()
    print(result)


def demo_schedule_optimization():
    """Demo: Schedule optimization"""
    print_section("DEMO 3: Schedule Optimization")
    
    system = ProductivitySystem()
    
    print("Creating optimized schedule for today...")
    today = datetime.now().strftime('%Y-%m-%d')
    result = system.optimize_my_schedule(date=today)
    print(result)


def demo_workflow_optimizer():
    """Demo: Custom Workflow Optimizer Tool"""
    print_section("DEMO 4: Custom Workflow Optimizer (Key Feature)")
    
    system = ProductivitySystem()
    
    # First, simulate some completed tasks for analysis
    print("Simulating workflow history...")
    from tools.workflow_optimizer import WorkflowOptimizerTool
    
    optimizer = WorkflowOptimizerTool()
    
    # Log some completed tasks
    for i in range(10):
        completion_data = {
            "action": "log",
            "user_id": "demo_user",
            "task_id": f"task_{i}",
            "task_name": f"Demo Task {i}",
            "completed_at": (datetime.now() - timedelta(days=10-i)).isoformat(),
            "duration_minutes": 45 + (i * 5),
            "priority": "high" if i < 3 else "medium",
            "was_on_time": i % 3 != 0  # Some tasks late
        }
        optimizer._run(json.dumps(completion_data))
    
    print("✓ Workflow history created")
    
    print("\nGetting personalized workflow insights...")
    result = system.get_workflow_insights(user_id="demo_user", time_range="week")
    print(result)


def demo_daily_planning():
    """Demo: Complete daily planning"""
    print_section("DEMO 5: Comprehensive Daily Planning")
    
    system = ProductivitySystem()
    
    print("Running complete daily planning workflow...")
    print("This coordinates all agents: Controller, Task Manager, and Schedule Optimizer")
    
    result = system.plan_my_day(focus_areas=["project work", "meetings"])
    print(result)


def demo_natural_language():
    """Demo: Natural language processing"""
    print_section("DEMO 6: Natural Language Request Processing")
    
    system = ProductivitySystem()
    
    requests = [
        "I have a big presentation next week. Help me prepare.",
        "What should I focus on today?",
        "I'm feeling overwhelmed with my task list. Can you help?"
    ]
    
    for i, request in enumerate(requests, 1):
        print(f"\nRequest {i}: '{request}'")
        print("-" * 70)
        result = system.process_natural_language_request(request)
        print(result)
        print()


def run_full_demo():
    """Run complete demo sequence"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "PERSONAL PRODUCTIVITY AGENTIC SYSTEM" + " " * 16 + "║")
    print("║" + " " * 23 + "Full System Demonstration" + " " * 20 + "║")
    print("╚" + "═" * 68 + "╝")
    
    demos = [
        ("Task Creation", demo_task_creation),
        ("Task Prioritization", demo_prioritization),
        ("Schedule Optimization", demo_schedule_optimization),
        ("Workflow Optimizer (Custom Tool)", demo_workflow_optimizer),
        ("Daily Planning", demo_daily_planning),
        ("Natural Language Processing", demo_natural_language)
    ]
    
    for name, demo_func in demos:
        try:
            demo_func()
            input(f"\n→ Press Enter to continue to next demo...")
        except KeyboardInterrupt:
            print("\n\nDemo interrupted by user.")
            break
        except Exception as e:
            print(f"\n✗ Error in {name}: {str(e)}")
            input("\n→ Press Enter to continue...")
    
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 22 + "Demo Complete! Thank you!" + " " * 20 + "║")
    print("╚" + "═" * 68 + "╝")
    print()


if __name__ == "__main__":
    print("""
    Demo Options:
    1. Run full demo (all features)
    2. Task creation only
    3. Prioritization only
    4. Schedule optimization only
    5. Workflow optimizer (custom tool)
    6. Daily planning
    7. Natural language processing
    
    """)
    
    choice = input("Select demo (1-7) [default: 1]: ").strip() or "1"
    
    if choice == "1":
        run_full_demo()
    elif choice == "2":
        demo_task_creation()
    elif choice == "3":
        demo_prioritization()
    elif choice == "4":
        demo_schedule_optimization()
    elif choice == "5":
        demo_workflow_optimizer()
    elif choice == "6":
        demo_daily_planning()
    elif choice == "7":
        demo_natural_language()
    else:
        print("Invalid choice. Running full demo...")
        run_full_demo()
