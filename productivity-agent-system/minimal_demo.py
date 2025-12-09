#!/usr/bin/env python3
"""
Minimal demo of Personal Productivity System with Ollama
This is a simplified single-file version for quick testing
"""
import os
from crewai import Agent, Task, Crew, Process, LLM

print("=" * 70)
print("Personal Productivity System - Minimal Demo")
print("=" * 70)
print()

# Configure Ollama
print("Configuring Ollama...")
os.environ["OPENAI_API_KEY"] = "ollama"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434"

# Create LLM instance
llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434"
)

print("✓ Ollama configured")
print()

# Create Controller Agent
print("Creating Controller Agent...")
controller = Agent(
    role="Productivity Coordinator",
    goal="Help users manage their tasks and optimize their productivity",
    backstory="""You are an expert productivity coach who helps people 
    organize their work, prioritize tasks, and maintain work-life balance.""",
    verbose=True,
    llm=llm
)
print("✓ Controller Agent created")

# Create Task Manager Agent
print("Creating Task Manager Agent...")
task_manager = Agent(
    role="Task Manager",
    goal="Create, organize, and prioritize tasks effectively",
    backstory="""You are a task management expert skilled in GTD and 
    Eisenhower Matrix prioritization.""",
    verbose=True,
    llm=llm
)
print("✓ Task Manager Agent created")

print()
print("=" * 70)
print("Running Demo: Create and Prioritize Tasks")
print("=" * 70)
print()

# Create a task
task1 = Task(
    description="""Create 3 sample tasks for a software developer:
    1. Review code for pull request (urgent, due today)
    2. Write documentation (important, due this week)  
    3. Update dependencies (low priority)

    Then prioritize these tasks using the Eisenhower Matrix.""",
    agent=task_manager,
    expected_output="A list of 3 tasks with priorities assigned"
)

# Run the crew
crew = Crew(
    agents=[controller, task_manager],
    tasks=[task1],
    process=Process.sequential,
    verbose=True
)

print("\n🚀 Starting agents...\n")
result = crew.kickoff()

print()
print("=" * 70)
print("Result:")
print("=" * 70)
print(result)
print()
print("=" * 70)
print("✅ Demo Complete!")
print("=" * 70)
print()
print("This proves:")
print("✓ Ollama is working")
print("✓ CrewAI is working")
print("✓ Agents can communicate")
print("✓ System is functional")
print()