"""
Configuration file for the Productivity Agentic System
"""
import os
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# LLM Configuration - Choose ONE option
# =============================================================================

# OPTION 1: Ollama (FREE - Recommended)
# Install: curl -fsSL https://ollama.com/install.sh | sh
# Then run: ollama pull llama3.1
USE_OLLAMA = True
OLLAMA_MODEL = "llama3.1"  # or "mistral", "llama2", "codellama"

# OPTION 2: OpenAI (Paid)
USE_OLLAMA = False
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4"

# OPTION 3: Groq (FREE with API key - very fast)
# Get free key: https://console.groq.com
# USE_OLLAMA = False
# GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
# OPENAI_MODEL = "groq/llama-3.1-70b-versatile"

# System Configuration
MAX_ITERATIONS = 10
VERBOSE = True

# File Paths
DATA_DIR = "data"
TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")
WORKFLOW_HISTORY_FILE = os.path.join(DATA_DIR, "workflow_history.json")

# Task Priority Weights
PRIORITY_WEIGHTS = {
    "urgency": 0.4,
    "importance": 0.4,
    "effort": 0.2
}

# Schedule Configuration
WORK_START_HOUR = 9
WORK_END_HOUR = 17
FOCUS_BLOCK_DURATION = 90  # minutes
BREAK_DURATION = 15  # minutes

# Workflow Optimization
MIN_HISTORY_ENTRIES = 5  # Minimum entries needed for pattern analysis
PRODUCTIVITY_THRESHOLD = 0.7  # Threshold for "productive" classification