"""
Synthetic RFM Dataset Generator
Creates larger synthetic datasets based on the existing RFM segmented data
"""

import pandas as pd
import numpy as np
from sklearn.utils import resample
import os

def analyze_original_data():
    """Analyze the original RFM dataset to understand its structure and distributions"""
    print("📊 Analyzing original RFM dataset...")
    
    # Load the original data
    df = pd.read_csv("data/rfm_segmented.csv")
    
    print(f"Original dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Analyze segment distribution
    segment_dist = df['Segment'].value_counts(normalize=True)
    print("\n📈 Segment Distribution:")
    for segment, pct in segment_dist.items():
        print(f"  • {segment}: {pct:.2%}")
    
    # Analyze score distributions
    print("\n📊 Score Distributions:")
    for score_col in ['R_score', 'F_score', 'M_score']:
        print(f"  • {score_col}: {df[score_col].value_counts().sort_index().to_dict()}")
    
    # Analyze numerical columns
    print("\n📈 Numerical Column Statistics:")
    numerical_cols = ['Recency', 'Frequency', 'Monetary']
    for col in numerical_cols:
        print(f"  • {col}: mean={df[col].mean():.2f}, std={df[col].std():.2f}, min={df[col].min():.2f}, max={df[col].max():.2f}")
    
    return df

def generate_synthetic_data(original_df, target_size, output_filename):
    """Generate synthetic RFM data based on the original dataset"""
    print(f"\n🔄 Generating synthetic dataset with {target_size:,} rows...")
    
    # Calculate how many times we need to oversample
    original_size = len(original_df)
    
    if target_size <= original_size:
        # If target is smaller, just sample
        synthetic_df = original_df.sample(n=target_size, random_state=42).copy()
    else:
        # Oversample by resampling with replacement and adding noise
        synthetic_rows = []
        
        # First, include all original data
        synthetic_rows.append(original_df.copy())
        remaining_rows = target_size - original_size
        
        # Generate additional rows by segment to maintain distribution
        segment_counts = original_df['Segment'].value_counts()
        
        for segment in segment_counts.index:
            segment_data = original_df[original_df['Segment'] == segment]
            segment_proportion = len(segment_data) / original_size
            segment_target = int(remaining_rows * segment_proportion)
            
            if segment_target > 0:
                # Resample with replacement
                resampled = resample(segment_data, n_samples=segment_target, random_state=42)
                
                # Add some noise to make it more realistic
                resampled_copy = resampled.copy()
                
                # Add noise to numerical columns
                for col in ['Recency', 'Frequency', 'Monetary']:
                    noise_std = resampled_copy[col].std() * 0.1  # 10% of std as noise
                    noise = np.random.normal(0, noise_std, len(resampled_copy))
                    resampled_copy[col] = np.maximum(0, resampled_copy[col] + noise)
                
                # Generate new CustomerIDs
                max_customer_id = original_df['CustomerID'].max()
                new_customer_ids = range(max_customer_id + 1, max_customer_id + 1 + len(resampled_copy))
                resampled_copy['CustomerID'] = new_customer_ids
                
                # Recalculate RFM_Score based on scores
                resampled_copy['RFM_Score'] = (
                    resampled_copy['R_score'].astype(str) + 
                    resampled_copy['F_score'].astype(str) + 
                    resampled_copy['M_score'].astype(str)
                )
                
                synthetic_rows.append(resampled_copy)
        
        # Combine all synthetic data
        synthetic_df = pd.concat(synthetic_rows, ignore_index=True)
        
        # If we have too many rows, randomly sample to exact target
        if len(synthetic_df) > target_size:
            synthetic_df = synthetic_df.sample(n=target_size, random_state=42).reset_index(drop=True)
    
    # Round numerical columns appropriately
    synthetic_df['Recency'] = synthetic_df['Recency'].round().astype(int)
    synthetic_df['Frequency'] = synthetic_df['Frequency'].round().astype(int)
    synthetic_df['Monetary'] = synthetic_df['Monetary'].round(2)
    
    # Ensure scores are within valid range (1-5)
    for score_col in ['R_score', 'F_score', 'M_score']:
        synthetic_df[score_col] = np.clip(synthetic_df[score_col], 1, 5).astype(int)
    
    # Recalculate RFM_Score to ensure consistency
    synthetic_df['RFM_Score'] = (
        synthetic_df['R_score'].astype(str) + 
        synthetic_df['F_score'].astype(str) + 
        synthetic_df['M_score'].astype(str)
    )
    
    # Save to file
    output_path = f"data/{output_filename}"
    synthetic_df.to_csv(output_path, index=False)
    
    print(f"✅ Synthetic dataset saved to: {output_path}")
    print(f"   Shape: {synthetic_df.shape}")
    
    # Verify segment distribution
    new_segment_dist = synthetic_df['Segment'].value_counts(normalize=True)
    print("   Segment Distribution:")
    for segment, pct in new_segment_dist.items():
        print(f"     • {segment}: {pct:.2%}")
    
    return synthetic_df

def main():
    """Main function to generate synthetic RFM datasets"""
    print("🚀 RFM Synthetic Dataset Generator")
    print("=" * 50)
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Analyze original data
    original_df = analyze_original_data()
    
    # Generate 10,000 row dataset
    print("\n" + "="*50)
    generate_synthetic_data(original_df, 10000, "rfm_segmented_10k.csv")
    
    # Generate 20,000 row dataset
    print("\n" + "="*50)
    generate_synthetic_data(original_df, 20000, "rfm_segmented_20k.csv")
    
    print("\n🎉 Synthetic dataset generation complete!")
    print("\nFiles created:")
    print("  • data/rfm_segmented_10k.csv (10,000 rows)")
    print("  • data/rfm_segmented_20k.csv (20,000 rows)")

if __name__ == "__main__":
    # Set random seed for reproducibility
    np.random.seed(42)
    main()
