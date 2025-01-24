import streamlit as st
import yfinance as yf
import pandas as pd
import warnings

def get_market_data():
    warnings.filterwarnings('ignore')
    
    tickers = ['USDBRL=X', '^BVSP', 'GC=F', '^GSPC', '^DJI', '^IXIC']
    data = yf.download(tickers, start='2025-01-01', auto_adjust=False, multi_level_index=False)

    pct_change = data['Adj Close'].pct_change().round(4) * 100

    symbols = ['Dólar', 'Ibovespa', 'Ouro', 'S&P 500', 'Dow Jones', 'Nasdaq']
    df = pd.DataFrame({
        'Symbol': symbols,
        'Value': [
            f"{data['Adj Close']['USDBRL=X'][-1]:.4f}",
            f"{data['Adj Close']['^BVSP'][-1]:.2f}",
            f"{data['Adj Close']['GC=F'][-1]:.2f}",
            f"{data['Adj Close']['^GSPC'][-1]:.2f}",
            f"{data['Adj Close']['^DJI'][-1]:.2f}",
            f"{data['Adj Close']['^IXIC'][-1]:.2f}"
        ],
        'Variação %': pct_change.iloc[-1].values
    })

    df['Variação %'] = df['Variação %'].apply(lambda x: f"+{x:.2f}%" if x > 0 else f"{x:.2f}%")

    df['Symbol'] = df.apply(lambda row: '↑ ' + row['Symbol'] if row['Variação %'][0] == '+' else '↓ ' + row['Symbol'], axis=1)
    
    return df

def color_rows(row):
    color = 'green' if row['Variação %'].startswith('↑') else 'red'
    return [f'color: {color}' for _ in row]

def main():
    st.set_page_config(page_title="Market Dashboard", page_icon="📈")
    
    st.title("Market Dashboard")
    
    try:
        df = get_market_data()
        
        # Style the dataframe
        styled_df = df.style.apply(color_rows, axis=1)
        
        # Display the dataframe
        st.dataframe(df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error fetching market data: {e}")

if __name__ == "__main__":
    main()