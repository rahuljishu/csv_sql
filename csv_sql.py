import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import io
from pandasql import sqldf

def main():
    st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")
    st.title("Interactive Data Analysis Dashboard")

    # File upload
    uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])
    
    if uploaded_file is not None:
        # Read CSV
        df = pd.read_csv(uploaded_file)
        
        # Basic Data Information
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Number of Rows", df.shape[0])
        with col2:
            st.metric("Number of Columns", df.shape[1])
        with col3:
            st.metric("Missing Values", df.isna().sum().sum())

        # Display sample data
        st.subheader("Sample Data")
        st.dataframe(df.head())

        # Data Summary
        st.subheader("Data Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Numerical Columns Summary")
            st.dataframe(df.describe())
        with col2:
            st.write("Columns Info")
            buffer = io.StringIO()
            df.info(buf=buffer)
            st.text(buffer.getvalue())

        # SQL Query Section
        st.subheader("SQL Query")
        query = st.text_area("Enter your SQL query:", "SELECT * FROM data LIMIT 5")
        if st.button("Run Query"):
            try:
                pysqldf = lambda q: sqldf(q, {'data': df})
                query_result = pysqldf(query)
                st.dataframe(query_result)
            except Exception as e:
                st.error(f"Error executing query: {str(e)}")

        # Visualization Section
        st.subheader("Create Visualization")
        
        # Chart type selection
        chart_type = st.selectbox(
            "Select Chart Type",
            ["Line Plot", "Bar Plot", "Scatter Plot", "Histogram"]
        )
        
        # Column selection based on chart type
        if chart_type in ["Line Plot", "Bar Plot"]:
            x_col = st.selectbox("Select X-axis column", df.columns)
            y_col = st.selectbox("Select Y-axis column", df.select_dtypes(include=['float64', 'int64']).columns)
            
            if chart_type == "Line Plot":
                fig = px.line(df, x=x_col, y=y_col)
            else:  # Bar Plot
                fig = px.bar(df, x=x_col, y=y_col)
                
        elif chart_type == "Scatter Plot":
            x_col = st.selectbox("Select X-axis column", df.select_dtypes(include=['float64', 'int64']).columns)
            y_col = st.selectbox("Select Y-axis column", df.select_dtypes(include=['float64', 'int64']).columns)
            color_col = st.selectbox("Select Color column (optional)", ["None"] + list(df.columns))
            
            if color_col == "None":
                fig = px.scatter(df, x=x_col, y=y_col)
            else:
                fig = px.scatter(df, x=x_col, y=y_col, color=color_col)
                
        else:  # Histogram
            col = st.selectbox("Select column", df.select_dtypes(include=['float64', 'int64']).columns)
            bins = st.slider("Number of bins", min_value=5, max_value=100, value=30)
            fig = px.histogram(df, x=col, nbins=bins)

        # Display the plot
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
