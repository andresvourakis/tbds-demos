"""
PandasAI Test Script for RFM Segmented Customer Data
This script demonstrates PandasAI capabilities with real customer segmentation data
"""

import os
from dotenv import load_dotenv
import pandasai as pai
from pandasai_openai.openai import OpenAI

# Load environment variables
load_dotenv()

def load_rfm_data():
    """Load the RFM segmented customer data"""
    print("📊 Loading RFM segmented customer data...")
    
    # Load the CSV file using PandasAI DataFrame
    df = pai.read_csv("data/rfm_segmented.csv")
    
    # Display basic information about the dataset
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\nFirst 5 rows:")
    print(df.head())
    
    print("\nDataset info:")
    print(f"- Total customers: {len(df)}")
    print(f"- Unique segments: {df['Segment'].nunique()}")
    print(f"- Segment distribution:")
    segment_counts = df['Segment'].value_counts()
    for segment, count in segment_counts.items():
        print(f"  • {segment}: {count} customers")
    
    return df

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

def test_basic_queries(df):
    """Test basic analytical queries without LLM"""
    print("\n🔍 Basic Data Analysis (without LLM):")
    
    # Basic statistics
    print(f"\nMonetary value statistics:")
    print(f"- Average: ${df['Monetary'].mean():.2f}")
    print(f"- Median: ${df['Monetary'].median():.2f}")
    print(f"- Max: ${df['Monetary'].max():.2f}")
    print(f"- Min: ${df['Monetary'].min():.2f}")
    
    print(f"\nFrequency statistics:")
    print(f"- Average purchases: {df['Frequency'].mean():.2f}")
    print(f"- Max purchases: {df['Frequency'].max()}")
    
    print(f"\nRecency statistics:")
    print(f"- Average days since last purchase: {df['Recency'].mean():.2f}")

def test_llm_queries(df, llm):
    """Test PandasAI chat functionality with sample queries"""
    if llm is None:
        print("\n⚠️  Skipping LLM queries - API key not configured")
        return
    
    print("\n🤖 Testing PandasAI Chat Functionality:")
    
    # Sample queries to test
    queries = [
        "How many customers are in each segment?",
        "What is the average monetary value for each customer segment?",
        "Which segment has the highest average frequency?",
        "Show me the top 5 customers by monetary value",
        "What percentage of customers are loyal customers?",
        "plot a bar chart displaying the distribution of customers accross the different segments",
        "plot a bar chart displaying the distribution of customers accross the different segments, each segment should be a different color, and the bars should be labeled with the customer count"
    ]
    
    for i, query in enumerate(queries, 1):
        try:
            print(f"\n{i}. Query: {query}")
            result = df.chat(query)
            print(f"   Answer: {result}")
        except Exception as e:
            print(f"   Error: {e}")

def interactive_mode(df, llm):
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
            print(f"Answer: {result}")
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main function to run the RFM data analysis"""
    print("🚀 PandasAI RFM Customer Segmentation Analysis")
    print("=" * 50)
    
    # Load the data
    df = load_rfm_data()
    
    # Setup LLM
    llm = setup_llm()
    
    # Run basic analysis
    test_basic_queries(df)
    
    # Test LLM queries
    test_llm_queries(df, llm)
    
    # Ask if user wants interactive mode
    if llm is not None:
        response = input("\nWould you like to try interactive mode? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            interactive_mode(df, llm)
    
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main()
