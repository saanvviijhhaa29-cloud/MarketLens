import os
import pandas as pd
import numpy as np

def load_nifty_data():
    
    file_paths = [
        r"C:\Users\okbro\Downloads\Marketlens\NIFTY 50\NIFTY 50-09-09-2020-to-09-09-2021.csv",
        r"C:\Users\okbro\Downloads\Marketlens\NIFTY 50\NIFTY 50-09-09-2021-to-09-09-2022.csv",
        r"C:\Users\okbro\Downloads\Marketlens\NIFTY 50\NIFTY 50-09-09-2022-to-09-09-2023.csv",
        r"C:\Users\okbro\Downloads\Marketlens\NIFTY 50\NIFTY 50-09-09-2023-to-09-09-2024.csv",
        r"C:\Users\okbro\Downloads\Marketlens\NIFTY 50\NIFTY 50-09-09-2024-to-09-09-2025.csv",
        r"C:\Users\okbro\Downloads\Marketlens\NIFTY 50\NIFTY 50-09-09-2025-to-9-09-2026.csv"
    ]
    
    df_list = []
    for path in file_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Target file missing: {path}")
            
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

def run_market_analysis():
    df = load_nifty_data()
    
   
    df['Daily_Return'] = df['Close'].pct_change()
    df['MA_50'] = df['Close'].rolling(window=50).mean()
    df['MA_200'] = df['Close'].rolling(window=200).mean()
    
    
    rolling_max = df['Close'].cummax()
    df['Drawdown_%'] = ((df['Close'] - rolling_max) / rolling_max) * 100
    
    start_date = df['Date'].min()
    end_date = df['Date'].max()
    start_close = df.iloc[0]['Close']
    end_close = df.iloc[-1]['Close']
    
    total_return = ((end_close - start_close) / start_close) * 100
    years = (end_date - start_date).days / 365.25
    cagr = (((end_close / start_close) ** (1 / years)) - 1) * 100
    
    print("=== NIFTY 50 Macro Market Analysis ===")
    print(f"Analysis Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"Total Trading Sessions: {len(df)}")
    print(f"Starting Index Value: {start_close}")
    print(f"Ending Index Value: {end_close}")
    print(f"Total Return: {total_return:.2f}%")
    print(f"CAGR: {cagr:.2f}%")
    print(f"All-Time High (Period): {df['Close'].max()}")
    print(f"Max Drawdown: {df['Drawdown_%'].min():.2f}%")
    
    return df

if __name__ == "__main__":
    market_df = run_market_analysis()