"""
Basic PandasAI example script
This demonstrates how to use PandasAI for data analysis
"""

import os
from dotenv import load_dotenv
import pandasai as pai
from pandasai_openai.openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Sample data for testing
sample_data = {
    "country": [
        "United States", "United Kingdom", "France", "Germany", "Italy", 
        "Spain", "Canada", "Australia", "Japan", "China"
    ],
    "revenue": [5000, 3200, 2900, 4100, 2300, 2100, 2500, 2600, 4500, 7000]
}

def test_basic_functionality():
    """Test basic PandasAI functionality without LLM"""
    print("Testing PandasAI basic functionality...")
    
    # Create a PandasAI DataFrame
    df = pai.DataFrame(sample_data)
    
    # Display basic info about the DataFrame
    print(f"DataFrame shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\nFirst few rows:")
    print(df.head())
    
    return df

def test_with_llm(df):
    """Test PandasAI with LLM (requires API key)"""
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key or api_key == 'your_openai_api_key_here':
        print("\n⚠️  OpenAI API key not found!")
        print("To use PandasAI chat functionality:")
        print("1. Get an OpenAI API key from https://platform.openai.com/")
        print("2. Add it to the .env file: OPENAI_API_KEY=your_actual_key")
        print("3. Run this script again")
        return
    
    try:
        print("\n🤖 Testing PandasAI chat functionality...")
        
        # Configure the LLM
        llm = OpenAI(api_key)
        pai.config.set({"llm": llm})
        
        # Test a simple query
        print("\nAsking: 'Which are the top 5 countries by revenue?'")
        result = df.chat('Which are the top 5 countries by revenue?')
        print(f"Answer: \n{result}")
        
        print("\n✅ PandasAI chat functionality is working!")
        
    except Exception as e:
        print(f"\n❌ Error testing LLM functionality: {e}")
        print("Make sure your OpenAI API key is valid and has sufficient credits.")

if __name__ == "__main__":
    # Test basic functionality
    df = test_basic_functionality()
    
    # Test LLM functionality if API key is available
    test_with_llm(df)
    
    print("\n✅ PandasAI setup verification complete!")
