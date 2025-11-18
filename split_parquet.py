#!/usr/bin/env python3
"""
Split a large parquet file into smaller files of approximately 1 million rows each.
Usage: python split_parquet.py <input_file> <output_dir> [chunk_size]
"""

import sys
import os
import pandas as pd
from pathlib import Path

def split_parquet(input_file, output_dir, chunk_size=1000000):
    """
    Split a parquet file into smaller files.
    
    Args:
        input_file: Path to input parquet file
        output_dir: Directory to save output files
        chunk_size: Number of rows per output file (default: 1,000,000)
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Get base filename without extension
    base_name = Path(input_file).stem
    
    print(f"Reading parquet file: {input_file}")
    print(f"Chunk size: {chunk_size:,} rows")
    print(f"Output directory: {output_dir}")
    print("-" * 60)
    
    # Read parquet file in chunks using pyarrow
    try:
        import pyarrow.parquet as pq
        
        # Open parquet file
        parquet_file = pq.ParquetFile(input_file)
        total_rows = parquet_file.metadata.num_rows
        print(f"Total rows in file: {total_rows:,}")
        
        # Calculate number of chunks needed
        num_chunks = (total_rows + chunk_size - 1) // chunk_size  # Ceiling division
        print(f"Will create {num_chunks} output files")
        print("-" * 60)
        
        # Read and write chunks
        for chunk_num in range(num_chunks):
            start_row = chunk_num * chunk_size
            end_row = min((chunk_num + 1) * chunk_size, total_rows)
            
            # Read chunk
            print(f"Processing chunk {chunk_num + 1}/{num_chunks} (rows {start_row:,} to {end_row:,})...", end=" ")
            
            # Read rows using pyarrow
            table = parquet_file.read_row_group(chunk_num // parquet_file.metadata.num_row_groups)
            # For simplicity, we'll use pandas to read in chunks
            # This is more memory efficient than reading the whole file
            
            # Read the specific range
            df_chunk = pd.read_parquet(input_file, engine='pyarrow')
            df_chunk = df_chunk.iloc[start_row:end_row]
            
            # Write chunk to new parquet file
            output_file = output_path / f"{base_name}_part_{chunk_num + 1:03d}.parquet"
            df_chunk.to_parquet(output_file, engine='pyarrow', index=False)
            
            print(f"✓ Saved {len(df_chunk):,} rows to {output_file.name}")
            
    except ImportError:
        # Fallback to pandas-only approach (less efficient but works)
        print("PyArrow not available, using pandas-only approach (may be slower)...")
        
        # Read parquet file in chunks
        # We'll use iter_batches if available, otherwise read in chunks manually
        chunk_num = 0
        start_row = 0
        
        while True:
            print(f"Reading chunk {chunk_num + 1} (starting at row {start_row:,})...", end=" ")
            
            # Read chunk
            df_chunk = pd.read_parquet(input_file, engine='auto')
            total_rows = len(df_chunk)
            
            # Process in chunks
            for i in range(0, total_rows, chunk_size):
                end_row = min(i + chunk_size, total_rows)
                df_part = df_chunk.iloc[i:end_row]
                
                output_file = output_path / f"{base_name}_part_{chunk_num + 1:03d}.parquet"
                df_part.to_parquet(output_file, engine='auto', index=False)
                
                print(f"✓ Saved {len(df_part):,} rows to {output_file.name}")
                
                chunk_num += 1
                
                if end_row >= total_rows:
                    break
            
            break  # Only one iteration needed
        
        print(f"\nTotal rows processed: {total_rows:,}")

def split_parquet_efficient(input_file, output_dir, chunk_size=1000000):
    """
    Memory-efficient version using pyarrow's row group reading.
    Reads one row group at a time and accumulates rows until reaching chunk_size.
    """
    import pyarrow.parquet as pq
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    base_name = Path(input_file).stem
    
    print(f"Reading parquet file: {input_file}")
    print(f"Chunk size: {chunk_size:,} rows")
    print(f"Output directory: {output_dir}")
    print("-" * 60)
    
    # Open parquet file
    parquet_file = pq.ParquetFile(input_file)
    total_rows = parquet_file.metadata.num_rows
    num_row_groups = parquet_file.num_row_groups
    
    print(f"Total rows in file: {total_rows:,}")
    print(f"Number of row groups: {num_row_groups}")
    
    # Calculate approximate number of chunks
    num_chunks = (total_rows + chunk_size - 1) // chunk_size
    print(f"Will create approximately {num_chunks} output files")
    print("-" * 60)
    
    chunk_num = 0
    current_chunk_dfs = []
    current_count = 0
    
    # Read row groups one at a time
    for row_group_idx in range(num_row_groups):
        print(f"Reading row group {row_group_idx + 1}/{num_row_groups}...", end=" ")
        
        # Read entire row group
        table = parquet_file.read_row_group(row_group_idx)
        df_group = table.to_pandas()
        
        print(f"loaded {len(df_group):,} rows")
        
        # Process rows from this group
        remaining_in_group = len(df_group)
        start_idx = 0
        
        while remaining_in_group > 0:
            # Calculate how many rows we can add to current chunk
            rows_needed = chunk_size - current_count
            rows_to_take = min(rows_needed, remaining_in_group)
            
            # Take rows from current group
            df_part = df_group.iloc[start_idx:start_idx + rows_to_take]
            current_chunk_dfs.append(df_part)
            current_count += len(df_part)
            
            # If we've filled a chunk, write it out
            if current_count >= chunk_size:
                df_chunk = pd.concat(current_chunk_dfs, ignore_index=True)
                output_file = output_path / f"{base_name}_part_{chunk_num + 1:03d}.parquet"
                df_chunk.to_parquet(output_file, engine='pyarrow', index=False)
                
                print(f"  ✓ Chunk {chunk_num + 1}: Saved {len(df_chunk):,} rows to {output_file.name}")
                
                chunk_num += 1
                current_chunk_dfs = []
                current_count = 0
            
            start_idx += rows_to_take
            remaining_in_group -= rows_to_take
    
    # Write remaining rows if any
    if current_chunk_dfs:
        df_chunk = pd.concat(current_chunk_dfs, ignore_index=True)
        output_file = output_path / f"{base_name}_part_{chunk_num + 1:03d}.parquet"
        df_chunk.to_parquet(output_file, engine='pyarrow', index=False)
        print(f"  ✓ Chunk {chunk_num + 1}: Saved {len(df_chunk):,} rows to {output_file.name}")
        chunk_num += 1
    
    print("-" * 60)
    print(f"Split complete! Created {chunk_num} files in {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python split_parquet.py <input_file> <output_dir> [chunk_size]")
        print("Example: python split_parquet.py data/file.parquet data/split 1000000")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    chunk_size = int(sys.argv[3]) if len(sys.argv) > 3 else 1000000
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        sys.exit(1)
    
    # Use the efficient version
    split_parquet_efficient(input_file, output_dir, chunk_size)

