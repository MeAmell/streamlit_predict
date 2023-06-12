import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    df = df[df["ConvertedComp"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedComp"] <= 250000]
    df = df[df["ConvertedComp"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    return df

df = load_data()



def show_explore_page():
    st.title("Informasi berdasarkan Data Survey Public")

    #st.write(
    ''''''
    #)

    st.write(""" # Jumlah Data dari berbagai Country""")

    data = df["Country"].value_counts()
    dataCountry = df["Country"]

    colors= ['#03045e4', '#262d79', '#475492', '#677bab', '#88a2c4', '#a9c9dd', '#caf0f6']
    
    # Membuat pie chart menggunakan Plotly
    fig = go.Figure(data=[go.Pie(labels=dataCountry, values=data, marker=dict(colors=colors))])
    fig.update_traces(textposition='inside', textinfo='label+percent')

    
    # Menampilkan pie chart menggunakan Streamlit
    st.plotly_chart(fig)
    #fig1, ax1 = plt.subplots(figsize=(11, 12))
    #ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    #ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    #st.pyplot(fig1)
    
    st.write(
        """
    # Rata-rata Gaji berdasarkan Negara
    """
    )

    #data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    #st.bar_chart(data)

    # Menghitung rata-rata gaji berdasarkan negara dan mengurutkannya
    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=False)

# Membuat bar chart menggunakan Plotly
    fig = go.Figure(data=go.Bar(
    x=data.index,  # Negara sebagai sumbu x
    y=data.values,  # Rata-rata gaji sebagai sumbu y
    marker=dict(color=data.values, colorscale='viridis'),  # Skema warna Inferno
))

# Menampilkan bar chart menggunakan Streamlit
    st.plotly_chart(fig)

    st.write(
        """
    # Rata-rata Gaji berdasarkan Pengalaman Kerja
    """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)

    #gabungan
     # Filter out rows with invalid "YearsCodePro" values
    st.write(""" # Rata-rata Pengalaman Kerja dan Salary berdasarkan Lulusan""")
    valid_years_code_pro = ['Less than 1 year', 'More than 50 years']
    df_filtered = df[~df['YearsCodePro'].isin(valid_years_code_pro)]

# Convert "YearsCodePro" column to float
    df_filtered['YearsCodePro'] = pd.to_numeric(df_filtered['YearsCodePro'], errors='coerce')

# Filter the dataframe for "Bachelor's degree" level
    bachelor_df = df_filtered[df_filtered['EdLevel'] == "Bachelor's degree"]

# Calculate the average YearsCodePro for "Bachelor's degree" level
    avg_years_code_pro_bachelor = bachelor_df['YearsCodePro'].mean()

# Data Anda
    ed_levels = df_filtered['EdLevel'].unique()
    years_code_pro = df_filtered.groupby('EdLevel')['YearsCodePro'].mean().reset_index()
    salary = df_filtered.groupby('EdLevel')['Salary'].mean().reset_index()

# Generate a color scale for each EdLevel
    color_scale = ['#0a2d2e', '#1c4e4f', '#436e6f', '#6a8e8f', '#879693',
              '#a49e97', '#deae9f', '#efd7cf', '#f7ebe7', '#fffff1']

# Membuat Bar Chart
    bar_chart = go.Bar(
        x=ed_levels,
        y=years_code_pro['YearsCodePro'],
        marker=dict(color=color_scale[:len(ed_levels)]),
        showlegend=False
)

# Membuat Line Chart
    line_chart = go.Scatter(
    x=ed_levels,
    y=salary['Salary'],
    name='Salary',
    yaxis='y2'
)

# Menggabungkan Bar Chart dan Line Chart
    data = [bar_chart, line_chart]

# Mengatur tata letak
    layout = go.Layout(
        yaxis=dict(title='YearsCodePro'),
        yaxis2=dict(title='Salary', overlaying='y', side='right'),
        xaxis=dict(showticklabels=False),
        legend=dict(
            x=0.5,
            y=1.15,
            orientation='h',
            bgcolor='rgba(0,0,0,0)'
    )
)

    # Membuat figure
    fig = go.Figure(data=data, layout=layout)

# Menampilkan kombinasi Bar Chart dan Line Chart dengan legenda
    st.plotly_chart(fig)

