# Testing PandasAI Project

This project is set up to test PandasAI functionality with Python 3.11, featuring both basic examples and real-world data analysis.

## Environment Setup

- **Python Version**: 3.11 (managed by Poetry)
- **PandasAI Version**: 3.0.0b19 (latest beta)
- **Dependency Management**: Poetry
- **LLM Integration**: OpenAI with configurable models

## Installation

1. Make sure you have Poetry installed
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Configure your OpenAI API key:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

## Available Scripts

### 1. `example.py` - Basic PandasAI Demo
A simple introduction to PandasAI functionality with sample data.

**Features:**
- Basic DataFrame operations
- Sample country/revenue data
- LLM setup instructions
- Environment variable configuration demo

**Usage:**
```bash
poetry run python example.py
```

### 2. `test_rfm_data.py` - Real Data Analysis
Comprehensive analysis script using real RFM customer segmentation data.

**Features:**
- Loads `data/rfm_segmented.csv` (customer segmentation dataset)
- Basic statistical analysis without LLM
- Pre-built analytical queries with LLM
- Interactive mode for custom questions
- Chart generation capabilities

**Sample Queries:**
- "How many customers are in each segment?"
- "What is the average monetary value for each customer segment?"
- "Plot a bar chart displaying the distribution of customers across segments"

**Usage:**
```bash
poetry run python test_rfm_data.py
```

### 3. `benchmark_rfm.py` - Performance Benchmarking
Compares PandasAI query performance across different dataset sizes (5K, 10K, 20K rows).

**Features:**
- **Multiple runs per query** (3 runs each) for reliable averages
- **Warmup queries** to eliminate first-connection slowness
- **Outlier detection** removes network timeout spikes (>2x median)
- **Progress tracking** shows which query is running
- **Transparent reporting** displays removed outliers

**What it tests:**
- Same 5 analytical queries on all three dataset sizes
- Measures end-to-end query time (API call + processing)
- Identifies whether dataset size impacts PandasAI performance

**Usage:**
```bash
poetry run python benchmark_rfm.py
```

**Sample Output:**
```
📈 BENCHMARK RESULTS
Query                                          5K (s)    10K (s)   20K (s)   
--------------------------------------------------------------------------------
How many customers are in each segment?        4.23      4.18      4.31
What is the average monetary value...          3.89      3.95      4.02
...
TOTAL                                         18.45     19.23     19.87
```

## Configuration

### OpenAI Model Selection
Configure your preferred model in `.env`:
```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-3.5-turbo  # or gpt-4, gpt-4-turbo
OPENAI_TEMPERATURE=0.7       # 0.0-1.0 range
```

**Supported Models:**
- `gpt-3.5-turbo` (default) - Fast, cost-effective
- `gpt-4` - More capable, higher cost
- `gpt-4-turbo` - Latest with improved performance

## Data

The project includes multiple RFM datasets for testing:

### Original Dataset
- `data/rfm_segmented.csv` - Original customer segmentation dataset (~4,334 rows)

### Synthetic Datasets
- `data/rfm_segmented_10k.csv` - Synthetic dataset with ~10,000 rows
- `data/rfm_segmented_20k.csv` - Synthetic dataset with ~20,000 rows

**Dataset Structure:**
- **CustomerID** - Unique customer identifier
- **Recency** - Days since last purchase
- **Frequency** - Number of purchases
- **Monetary** - Total purchase value
- **R_score, F_score, M_score** - RFM scores (1-5 scale)
- **RFM_Score** - Combined score string (e.g., "355")
- **Segment** - Customer segment (e.g., "Loyal Customers", "At Risk")

**Customer Segments:**
- Best Customers (~21.6%)
- Others (~40.9%)
- Loyal Customers (~17.7%)
- Recent but Infrequent (~7.3%)
- At Risk (~6.6%)
- Lost Customers (~4.3%)
- Big Spenders (New) (~1.6%)

## Requirements

- Python 3.11
- Poetry for dependency management
- OpenAI API key (for LLM functionality)
- Internet connection (for API calls)

## Getting Started

1. **Quick Start**: Run `poetry run python example.py` for basic functionality
2. **Real Data Analysis**: Run `poetry run python test_rfm_data.py` for comprehensive testing
3. **Interactive Mode**: Use the interactive mode in `test_rfm_data.py` to ask custom questions about your data
