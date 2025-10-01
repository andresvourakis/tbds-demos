import streamlit as st
import pandas as pd
import numpy as np

st.title("Streamlit Dashboard")

st.write("Here are some example charts:")

# Create some sample data
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

# Display a line chart
st.subheader("Line Chart")
st.line_chart(chart_data)

# Display a bar chart
st.subheader("Bar Chart")
st.bar_chart(chart_data)

# Display a map
st.subheader("Map")
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
st.map(map_data)
