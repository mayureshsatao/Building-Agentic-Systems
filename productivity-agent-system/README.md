# Personal Productivity Agentic System

A sophisticated multi-agent AI system built with CrewAI that helps manage tasks, optimize schedules, and improve personal productivity through intelligent workflow analysis.

## 🎯 Project Overview

This system demonstrates advanced agentic AI architecture with:
- **4 Specialized Agents**: Controller, Task Manager, Schedule Optimizer, and Information Curator
- **3 Built-in Tools**: Web Search (SerperDevTool), Date Calculator, File Processor
- **1 Custom Tool**: Workflow Optimizer (analyzes productivity patterns and provides personalized recommendations)
- **Multi-agent Orchestration**: Sequential and hierarchical task delegation

## 📋 Features

### Core Capabilities
- ✅ **Task Management**: Create, prioritize, and track tasks using proven frameworks (Eisenhower Matrix, MoSCoW)
- ✅ **Schedule Optimization**: Find optimal time slots, prevent conflicts, and balance workload
- ✅ **Workflow Intelligence**: Analyze productivity patterns and provide personalized recommendations
- ✅ **Natural Language Processing**: Understand and execute complex productivity requests
- ✅ **Data Persistence**: Store and retrieve tasks and workflow history

### Custom Tool: Workflow Optimizer
Our custom tool analyzes your work patterns to provide actionable insights:
- Identifies most productive hours
- Detects procrastination patterns
- Calculates productivity scores
- Recommends optimal task batching
- Suggests break schedules based on focus patterns

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- OpenAI API key
- (Optional) Serper API key for web search

### Setup Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd productivity-agent-system
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here  # Optional
```

5. **Initialize data directory**
```bash
mkdir -p data
```

## 📖 Usage

### Basic Usage

```python
from main import ProductivitySystem

# Initialize the system
system = ProductivitySystem()

# Create a task
system.create_task(
    title="Complete project proposal",
    description="Write Q4 proposal",
    priority="high",
    deadline="2024-12-01",
    estimated_duration=120,
    tags=["work", "urgent"]
)

# Get daily plan
result = system.plan_my_day()
print(result)

# Get workflow insights
insights = system.get_workflow_insights()
print(insights)
```

### Command-Line Usage

```bash
# Run the main application
python main.py

# Run demo script
python demo/demo_script.py

# Run tests
python tests/test_system.py
```

## 🏗️ System Architecture

### Agent Hierarchy

```
Controller Agent (Coordinator)
├── Task Manager Agent
│   ├── File Processor Tool
│   ├── Date Calculator Tool
│   └── Prioritization Tool
├── Schedule Optimizer Agent
│   ├── Date Calculator Tool
│   └── File Processor Tool
└── Information Curator Agent
    ├── Web Search Tool
    └── File Processor Tool
```

### Agent Descriptions

#### 1. Controller Agent
- **Role**: System orchestrator
- **Responsibilities**: 
  - Analyzes user requests
  - Delegates to specialized agents
  - Aggregates results
  - Handles errors and fallbacks

#### 2. Task Manager Agent
- **Role**: Task management specialist
- **Responsibilities**:
  - Creates and organizes tasks
  - Applies prioritization frameworks
  - Tracks task progress
  - Manages deadlines

#### 3. Schedule Optimizer Agent
- **Role**: Time management expert
- **Responsibilities**:
  - Finds available time slots
  - Optimizes schedule allocation
  - Detects scheduling conflicts
  - Balances workload

#### 4. Information Curator Agent
- **Role**: Knowledge management specialist
- **Responsibilities**:
  - Organizes information
  - Retrieves relevant context
  - Searches for resources
  - Maintains knowledge base

## 🛠️ Tools

### Built-in Tools

1. **Date Calculator Tool**
   - Calculate days until deadline
   - Check scheduling conflicts
   - Find available time slots
   - Calculate working days

2. **File Processor Tool**
   - Load/save tasks to JSON
   - Update task status
   - Generate reports
   - Export data in various formats

3. **Web Search Tool** (Optional)
   - Search for productivity tips
   - Find relevant resources
   - Research best practices

### Custom Tool: Workflow Optimizer

**Purpose**: Analyzes productivity patterns to provide personalized optimization recommendations.

**Inputs**:
- Task completion history
- Work patterns and timestamps
- Priority levels and deadlines
- User preferences

**Outputs**:
- Productivity score (0-1)
- Best productivity hours
- Procrastination score
- Focus pattern analysis
- Personalized recommendations

**Key Features**:
- Pattern recognition in task completion
- Time-of-day productivity analysis
- Focus duration tracking
- Consistency scoring
- Actionable recommendations

**Example Usage**:
```python
from tools.workflow_optimizer import WorkflowOptimizerTool

optimizer = WorkflowOptimizerTool()

# Analyze patterns
result = optimizer._run(json.dumps({
    "action": "analyze",
    "user_id": "user123",
    "time_range": "week"
}))

# Get recommendations
recommendations = optimizer._run(json.dumps({
    "action": "recommend",
    "user_id": "user123",
    "time_range": "week"
}))
```

## 🧪 Testing

### Run All Tests
```bash
python tests/test_system.py
```

### Test Coverage
- ✅ Workflow Optimizer functionality
- ✅ Date Calculator operations
- ✅ File Processor CRUD operations
- ✅ End-to-end integration workflow

### Example Test Results
```
Ran 15 tests in 2.345s
OK (successes=15)
```

## 📊 Evaluation Metrics

### Performance Metrics
- **Response Time**: Average agent response time < 5 seconds
- **Accuracy**: Task prioritization accuracy > 85%
- **Reliability**: System uptime > 99%

### Effectiveness Metrics
- **User Satisfaction**: Based on result quality
- **Time Saved**: Estimated weekly time savings
- **Task Completion Rate**: Improvement in on-time completions
- **Workflow Optimization**: Adoption rate of recommendations

### Technical Metrics
- **Tool Usage**: Distribution of tool calls
- **Agent Coordination**: Successful delegation rate
- **Memory Efficiency**: Context retrieval accuracy
- **Error Rate**: Failed operations per 100 requests

## 🎥 Demo Video

The demo script showcases:
1. Task creation and management
2. Intelligent prioritization
3. Schedule optimization
4. Custom Workflow Optimizer in action
5. Complete daily planning workflow
6. Natural language request processing

Run the demo:
```bash
python demo/demo_script.py
```

## 📚 Documentation

### Key Files
- `main.py`: Main application and ProductivitySystem class
- `config.py`: Configuration and settings
- `agents/`: Agent definitions and configurations
- `tools/`: Tool implementations (built-in and custom)
- `data/`: Data storage (tasks, workflow history)
- `tests/`: Test suite
- `demo/`: Demonstration scripts

### Configuration Options
Edit `config.py` to customize:
- Work hours (default: 9 AM - 5 PM)
- Focus block duration (default: 90 minutes)
- Priority weights
- Productivity thresholds

## 🔧 Troubleshooting

### Common Issues

**Issue**: "OPENAI_API_KEY not found"
- **Solution**: Create `.env` file with your API key

**Issue**: Web search not working
- **Solution**: Add SERPER_API_KEY to `.env` or system works without it

**Issue**: No tasks file found
- **Solution**: System auto-creates on first run, or run `mkdir data`

**Issue**: Import errors
- **Solution**: Ensure virtual environment is activated and dependencies installed

## 🚀 Future Enhancements

- [ ] Integration with calendar APIs (Google Calendar, Outlook)
- [ ] Mobile app interface
- [ ] Team collaboration features
- [ ] Advanced analytics dashboard
- [ ] Machine learning for adaptive prioritization
- [ ] Voice command interface
- [ ] Integration with project management tools (Jira, Asana)

## 📄 License

This project is created for educational purposes as part of the Building Agentic Systems assignment.

## 👥 Contributors

- [Your Name] - Initial implementation and design

## 🙏 Acknowledgments

- CrewAI framework for multi-agent orchestration
- OpenAI for language model capabilities
- Assignment guidelines for project direction

---

**Built with ❤️ using CrewAI and Python**
