import os
import pandas as pd
import numpy as np

def load_bank_sector_data():
    """
    Loads and merges the NIFTY BANK sector datasets.
    """
    file_paths = [
        r"C:\Users\okbro\Downloads\Marketlens\sector\NIFTY BANK\NIFTY BANK-09-09-2024-to-09-09-2025.csv",
        r"C:\Users\okbro\Downloads\Marketlens\sector\NIFTY BANK\NIFTY BANK-9-09-2025-to-9-09-2026.csv"
    ]
    
    df_list = []
    for path in file_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Sector file missing: {path}")
            
        temp = pd.read_csv(path)
        temp.columns = [c.strip() for c in temp.columns]
        temp['Date'] = pd.to_datetime(temp['Date'], format='%d-%b-%Y', errors='coerce')
        df_list.append(temp)
        
    combined_df = pd.concat(df_list).drop_duplicates(subset=['Date']).sort_values('Date').reset_index(drop=True)
    
   
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Shares Traded', 'Turnover (₹ Cr)']
    for col in numeric_cols:
        if col in combined_df.columns:
            combined_df[col] = pd.to_numeric(combined_df[col].astype(str).str.replace(',', ''), errors='coerce')
            
    return combined_df

