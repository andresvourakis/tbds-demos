# Data Cleaning Agent

An LLM-powered agent that automatically generates and executes Python code to clean messy datasets. Built with LangChain and LangGraph.

## How It Works

1. **Analyze** - Examines your dataset structure and data quality issues
2. **Generate** - LLM creates custom Python cleaning code
3. **Execute** - Runs the generated code on your data
4. **Self-Correct** - Automatically fixes errors (up to 3 retries)

## Setup

### Prerequisites

- Python 3.9+ (except 3.9.7)
- Poetry
- OpenAI API key

### Installation

1. **Install dependencies**:
   ```bash
   poetry install
   ```

2. **Set up API key**:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your OpenAI API key.

## Usage

### Python API

```python
import pandas as pd
from langchain_openai import ChatOpenAI
from data_cleaning_agent import LightweightDataCleaningAgent

# Initialize agent
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
agent = LightweightDataCleaningAgent(model=llm)

# Clean your data
df = pd.read_csv("your_data.csv")
agent.invoke_agent(data_raw=df)
cleaned_df = agent.get_data_cleaned()
```

**Custom instructions** (optional):
```python
agent.invoke_agent(
    data_raw=df,
    user_instructions="Remove columns with >30% missing values"
)
```

## Project Structure

```
data-cleaning-agent/
├── data_cleaning_agent/
│   ├── data_cleaning_agent.py  # Main agent
│   ├── graph.py                # LangGraph workflow
│   └── utils.py                # Helper functions
├── pyproject.toml              # Dependencies
└── .env                        # API keys
```
