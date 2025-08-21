# %%
"""
PandasAI Interactive Test Script for RFM Segmented Customer Data
This script is structured like a Jupyter notebook with cell separators
Run each cell (# %%) individually to see results step by step
"""

import os
from dotenv import load_dotenv
import pandasai as pai
from pandasai_openai.openai import OpenAI

# Load environment variables
load_dotenv()

# %%
# Cell 1: Load and explore the RFM data
print("📊 Loading RFM segmented customer data...")

# Load the CSV file using PandasAI DataFrame
df = pai.read_csv("data/rfm_segmented.csv")

# Display basic information about the dataset
print(f"Dataset shape: {df.shape}")
print(f"Columns: {list(df.columns)}")

# %%
# Cell 2: Show first few rows and basic info
print("First 5 rows:")
print(df.head())

print("\nDataset info:")
print(f"- Total customers: {len(df)}")
print(f"- Unique segments: {df['Segment'].nunique()}")

# %%
# Cell 3: Segment distribution analysis
print("Segment distribution:")
segment_counts = df['Segment'].value_counts()
for segment, count in segment_counts.items():
    print(f"  • {segment}: {count} customers")

# %%
# Cell 4: Setup LLM configuration
def setup_llm():
    """Setup the LLM for PandasAI chat functionality"""
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key or api_key == 'your_openai_api_key_here':
        print("\n⚠️  OpenAI API key not configured!")
        print("Add your API key to .env file: OPENAI_API_KEY=your_actual_key")
        return None
    
    # Get model and temperature from environment variables with defaults
    model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')  # Default: gpt-3.5-turbo
    temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))  # Default: 0.7
    
    try:
        print(f"\n🤖 Configuring OpenAI LLM:")
        print(f"   Model: {model}")
        print(f"   Temperature: {temperature}")
        
        llm = OpenAI(api_key=api_key, model=model, temperature=temperature)
        pai.config.set({"llm": llm})
        print("✅ LLM configured successfully!")
        return llm
    except Exception as e:
        print(f"❌ Error configuring LLM: {e}")
        return None

# Setup the LLM
llm = setup_llm()

# %%
# Cell 5: Basic data analysis (without LLM)
print("🔍 Basic Data Analysis (without LLM):")

# Basic statistics
print(f"\nMonetary value statistics:")
print(f"- Average: ${df['Monetary'].mean():.2f}")
print(f"- Median: ${df['Monetary'].median():.2f}")
print(f"- Max: ${df['Monetary'].max():.2f}")
print(f"- Min: ${df['Monetary'].min():.2f}")

# %%
# Cell 6: More basic statistics
print(f"Frequency statistics:")
print(f"- Average purchases: {df['Frequency'].mean():.2f}")
print(f"- Max purchases: {df['Frequency'].max()}")

print(f"\nRecency statistics:")
print(f"- Average days since last purchase: {df['Recency'].mean():.2f}")

# %%
# Cell 7: Test LLM Query 1 - Segment counts
if llm is not None:
    print("🤖 Query 1: How many customers are in each segment?")
    try:
        result = df.chat("How many customers are in each segment?")
        print(f"\nAnswer:\n{result}\n")
    except Exception as e:
        print(f"\nError: {e}\n")
else:
    print("⚠️ Skipping LLM queries - API key not configured")

# %%
# Cell 8: Test LLM Query 2 - Average monetary value
if llm is not None:
    print("🤖 Query 2: What is the average monetary value for each customer segment?")
    try:
        result = df.chat("What is the average monetary value for each customer segment?")
        print(f"\nAnswer:\n{result}\n")
    except Exception as e:
        print(f"\nError: {e}\n")

# %%
# Cell 9: Test LLM Query 3 - Highest frequency segment
if llm is not None:
    print("🤖 Query 3: Which segment has the highest average frequency?")
    try:
        result = df.chat("Which segment has the highest average frequency?")
        print(f"\nAnswer:\n{result}\n")
    except Exception as e:
        print(f"\nError: {e}\n")

# %%
# Cell 10: Test LLM Query 4 - Top customers
if llm is not None:
    print("🤖 Query 4: Show me the top 5 customers by monetary value")
    try:
        result = df.chat("Show me the top 5 customers by monetary value")
        print(f"\nAnswer:\n{result}\n")
    except Exception as e:
        print(f"\nError: {e}\n")

# %%
# Cell 11: Test LLM Query 5 - Loyal customers percentage
if llm is not None:
    print("🤖 Query 5: What percentage of customers are loyal customers?")
    try:
        result = df.chat("What percentage of customers are loyal customers?")
        print(f"\nAnswer:\n{result}\n")
    except Exception as e:
        print(f"\nError: {e}\n")

# %%
# Cell 12: Test visualization query
if llm is not None:
    print("🤖 Query 6: Plot a bar chart displaying the distribution of customers across segments")
    try:
        result = df.chat("plot a bar chart displaying the distribution of customers across the different segments")
        print(f"\nAnswer:\n{result}\n")
    except Exception as e:
        print(f"\nError: {e}\n")

# %%
# Cell 13: Test advanced visualization query
if llm is not None:
    print("🤖 Query 7: Plot a colorful bar chart with labels")
    try:
        result = df.chat("plot a bar chart displaying the distribution of customers across the different segments, each segment should be a different color, and the bars should be labeled with the customer count")
        print(f"\nAnswer:\n{result}\n")
    except Exception as e:
        print(f"\nError: {e}\n")

# %%
# Cell 14: Interactive mode function (optional)
def interactive_mode():
    """Interactive mode for custom queries"""
    if llm is None:
        print("\n⚠️  Interactive mode requires OpenAI API key")
        return
    
    print("\n🎯 Interactive Mode - Ask your own questions!")
    print("Type 'quit' to exit")
    
    while True:
        query = input("\nYour question: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("Goodbye! 👋")
            break
        
        if not query:
            continue
            
        try:
            result = df.chat(query)
            print(f"\nAnswer:\n{result}\n")
        except Exception as e:
            print(f"\nError: {e}\n")

# Uncomment the line below to start interactive mode
# interactive_mode()

# %%
print("✅ Interactive analysis complete!")
print("\nTo use this script:")
print("1. Run each cell (# %%) individually in VS Code or similar editor")
print("2. Or uncomment interactive_mode() above for custom queries")
