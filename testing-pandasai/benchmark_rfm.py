"""
PandasAI Benchmarking Script
Simple latency comparison across different dataset sizes (5k, 10k, 20k rows)
"""

import os
import time
from dotenv import load_dotenv
import pandasai as pai
from pandasai_openai.openai import OpenAI

# Load environment variables
load_dotenv()

def setup_llm():
    """Setup the LLM for PandasAI"""
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key or api_key == 'your_openai_api_key_here':
        print("❌ OpenAI API key not configured!")
        return None
    
    model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
    
    llm = OpenAI(api_key=api_key, model=model, temperature=temperature)
    pai.config.set({"llm": llm})
    return llm

def load_dataset(filename):
    """Load a dataset and return PandasAI DataFrame"""
    return pai.read_csv(f"data/{filename}")

def remove_outliers(times):
    """Simple outlier removal: remove values > 2x median"""
    if not times:
        return []
    
    # Calculate median time from sorted list
    median = sorted(times)[len(times)//2]
    
    # Set threshold: anything > 2x median is considered an outlier
    # This catches network timeouts like the 83s spike we saw
    threshold = median * 2
    
    # Filter out outliers (times above threshold)
    filtered = [t for t in times if t <= threshold]
    
    # Safety: always keep at least 1 result (the fastest time)
    return filtered if filtered else [min(times)]

def benchmark_queries(df, dataset_name, runs=3):
    """Run benchmark queries multiple times and measure average time"""
    # Standard queries to test across all datasets
    queries = [
        "How many customers are in each segment?",
        "What is the average monetary value for each customer segment?",
        "Which segment has the highest average frequency?",
        "Show me the top 5 customers by monetary value",
        "What percentage of customers are loyal customers?"
    ]
    
    # WARMUP: First API call is often slower due to connection setup
    # Run a simple query to "warm up" the connection before benchmarking
    print(f"   Warming up...")
    try:
        df.chat("How many rows are in this dataset?")
    except:
        pass  # Ignore warmup errors
    
    results = []
    
    # MAIN BENCHMARK LOOP: Test each query multiple times
    for i, query in enumerate(queries, 1):
        print(f"   Query {i}/{len(queries)}: Running {runs} times...")
        times = []  # Store execution times for this query
        
        # MULTIPLE RUNS: Run same query multiple times to get reliable average
        for run in range(runs):
            start_time = time.time()
            try:
                # Execute the query (this is what we're timing)
                df.chat(query)
                end_time = time.time()
                duration = end_time - start_time
                times.append(duration)
            except Exception as e:
                print(f"     Run {run+1} error: {e}")
                # Continue with other runs even if one fails
        
        # PROCESS RESULTS: Calculate average after removing outliers
        if times:
            # Remove network timeout outliers (like that 83s spike)
            filtered_times = remove_outliers(times)
            
            # Calculate average of clean times
            avg_time = sum(filtered_times) / len(filtered_times)
            
            # TRANSPARENCY: Show user if outliers were removed
            if len(filtered_times) < len(times):
                removed = [t for t in times if t not in filtered_times]
                print(f"     Removed outliers: {removed} seconds")
            
            results.append(avg_time)
        else:
            # All runs failed for this query
            results.append(None)
    
    return results

def main():
    """Main benchmarking function"""
    print("🚀 PandasAI Latency Benchmark")
    print("=" * 40)
    
    # SETUP: Configure OpenAI LLM for PandasAI
    llm = setup_llm()
    if llm is None:
        return
    
    # DATASETS: Define the three dataset sizes to compare
    datasets = [
        ("rfm_segmented.csv", "5K Dataset"),      # ~4,334 rows (original)
        ("rfm_segmented_10k.csv", "10K Dataset"),  # ~10,000 rows (synthetic)
        ("rfm_segmented_20k.csv", "20K Dataset")   # ~20,000 rows (synthetic)
    ]
    
    # QUERIES: Same queries tested on all datasets for comparison
    queries = [
        "How many customers are in each segment?",
        "What is the average monetary value for each customer segment?",
        "Which segment has the highest average frequency?",
        "Show me the top 5 customers by monetary value",
        "What percentage of customers are loyal customers?"
    ]
    
    all_results = {}  # Store results for all datasets
    
    # MAIN BENCHMARK: Test each dataset size
    for filename, dataset_name in datasets:
        print(f"\n📊 Testing {dataset_name}...")
        
        # Load the dataset into PandasAI DataFrame
        df = load_dataset(filename)
        print(f"   Loaded {len(df)} rows")
        
        # Run the benchmark (multiple runs per query, with outlier removal)
        results = benchmark_queries(df, dataset_name)
        all_results[dataset_name] = results
        
        # Show summary for this dataset
        total_time = sum(r for r in results if r is not None)
        print(f"   Total time: {total_time:.2f}s (average of multiple runs)")
    
    # Print comparison results
    print("\n" + "=" * 40)
    print("📈 BENCHMARK RESULTS")
    print("=" * 40)
    
    print(f"{'Query':<50} {'5K (s)':<10} {'10K (s)':<10} {'20K (s)':<10}")
    print("-" * 80)
    
    for i, query in enumerate(queries):
        row = f"{query[:47]+'...' if len(query) > 47 else query:<50}"
        for dataset_name in ["5K Dataset", "10K Dataset", "20K Dataset"]:
            time_val = all_results[dataset_name][i]
            if time_val is not None:
                row += f"{time_val:<10.2f}"
            else:
                row += f"{'ERROR':<10}"
        print(row)
    
    # Print totals
    print("-" * 80)
    totals_row = f"{'TOTAL':<50}"
    for dataset_name in ["5K Dataset", "10K Dataset", "20K Dataset"]:
        total = sum(r for r in all_results[dataset_name] if r is not None)
        totals_row += f"{total:<10.2f}"
    print(totals_row)
    
    print("\n✅ Benchmark complete!")

if __name__ == "__main__":
    main()
