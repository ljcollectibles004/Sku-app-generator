import streamlit as st
import pandas as pd
import io

# App Layout
st.set_page_config(page_title="Bulk SKU Generator", page_icon="📦")
st.title("📦 Bulk SKU Auto-Assigner")
st.write("Upload a CSV to automatically generate SKUs categorized by Lot.")

# 1. Upload File
uploaded_file = st.file_uploader("Upload your items CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.subheader("Data Preview")
    st.dataframe(df.head())

    # 2. Configuration
    columns = df.columns.tolist()
    
    col1, col2 = st.columns(2)
    with col1:
        lot_col = st.selectbox("Select the 'Lot' column:", options=columns)
    with col2:
        sku_prefix = st.text_input("SKU Prefix (Optional):", value="INV-")

    # 3. Process Data
    if st.button("Generate & Preview SKUs"):
        # Sort to keep lots together
        df = df.sort_values(by=lot_col)
        
        # Create a counter for each item within a lot
        df['item_num'] = df.groupby(lot_col).cumcount() + 1
        
        # Create the SKU: Prefix + Lot + 001, 002, etc.
        df['SKU'] = (sku_prefix + 
                     df[lot_col].astype(str) + "-" + 
                     df['item_num'].astype(str).str.zfill(3))
        
        # Remove temporary column
        df_final = df.drop(columns=['item_num'])
        
        st.success("SKUs Generated!")
        st.dataframe(df_final)

        # 4. Download Result
        csv_buffer = io.StringIO()
        df_final.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Download Updated CSV",
            data=csv_buffer.getvalue(),
            file_name="processed_inventory.csv",
            mime="text/csv"
        )
      
