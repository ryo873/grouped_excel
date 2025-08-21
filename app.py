import streamlit as st
import pandas as pd
from io import BytesIO
import time

# Page configuration
st.set_page_config(
    page_title="Excel Data Classifier",
    page_icon="📊",
    layout="wide"
)

# App title
st.title("📊 Grouped by Type")
st.markdown("Upload an Excel file to group data by **Type** and **Object Name** columns")

# Sidebar for file upload
with st.sidebar:
    st.header("📁 Upload File")
    uploaded_file = st.file_uploader(
        "Choose an Excel file",
        type=['xlsx', 'xls'],
        help="File must contain 'Type' and 'Object Name' columns"
    )

    if uploaded_file is not None:
        if uploaded_file.size > 100 * 1024 * 1024:  # 100MB
            st.error("File size too large. Please upload files under 100MB")
    
    # Options
    st.header("⚙️ Options")
    separator = st.text_input("Separator for combined values", " OR ")
    output_filename = st.text_input("Output file name", "classified_result.xlsx")

@st.cache_data
# Function to process data
def process_excel_data(file, separator):
    try:
        # Read Excel file
        df = pd.read_excel(file)
        
        # Validate required columns
        required_columns = ['Type', 'Object Name']
        if not all(col in df.columns for col in required_columns):
            st.error(f"File must contain columns: {required_columns}")
            return None, None
        
        # Grouping data
        def join_unique(values):
            unique_values = list(set(values))
            return separator.join(unique_values)
        
        grouped = df.groupby('Type')['Object Name'].agg(join_unique).reset_index()
        
        return df, grouped
        
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None, None

# Main content
if uploaded_file is not None:
    # Process data
    with st.spinner('Processing data...'):
        raw_df, grouped_df = process_excel_data(uploaded_file, separator)
        time.sleep(1)  # Simulated processing time
    
    if raw_df is not None and grouped_df is not None:
        # Show preview of data
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📄 Original Data")
            st.dataframe(raw_df, use_container_width=True)
            st.caption(f"Total rows: {len(raw_df)}")
        
        with col2:
            st.subheader("🎯 Grouped Result")
            st.dataframe(grouped_df, use_container_width=True)
            st.caption(f"Total groups: {len(grouped_df)}")
        
        # Download section
        st.divider()
        st.subheader("📥 Download Result")
        
        # Convert grouped data to Excel for download
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            grouped_df.to_excel(writer, sheet_name='Grouped Data', index=False)
            raw_df.to_excel(writer, sheet_name='Raw Data', index=False)
        
        output.seek(0)
        
        # Download button
        st.download_button(
            label="📥 Download Excel Result",
            data=output,
            file_name=output_filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Click to download grouped results"
        )
        
        # Success message
        st.success("✅ Data successfully processed! You can now download the result.")

else:
    # Placeholder when no file is uploaded
    st.info("👈 Please upload an Excel file via the sidebar on the left")
    
    # Example data preview
    st.subheader("📋 Example of Required Data Format")
    example_data = {
        'Type': ['Application', 'Integration Object', 'Business Component', 'Application'],
        'Object Name': ['Siebel Financial Services', 'FCC Saving More Info_1 VBC IO', 
                       'FCC Saving More Info_1 VBC', 'Siebel Financial Services']
    }
    example_df = pd.DataFrame(example_data)
    st.dataframe(example_df, use_container_width=True)

# Footer
st.divider()
st.caption("© 2024 Excel Data Classifier - Built with Streamlit")
