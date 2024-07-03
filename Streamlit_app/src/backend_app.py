#Author: Alberto Moccardi
# Version: 1.0  
# Date: 2024-07-08
# Deep Learning for predictive maintenance course

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import joblib
import time
from plotly.subplots import make_subplots

def load_model(path):
    return joblib.load(path)

def load_data_from_db(db_path, table_name='users'):
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql(f'SELECT * FROM {table_name}', conn)

def insert_data_from_csv(db_path, csv_file):
    try:
        with sqlite3.connect(db_path) as conn:
            df = pd.read_csv(csv_file)
            df.to_sql('users', conn, if_exists='append', index=False)
        return True
    except Exception as e:
        st.error(f"Failed to insert data: {e}")
        return False

def plot_clusters(data):
    fig = px.bar(data['Cluster'].value_counts().sort_index(), title='Count of People per Cluster')
    fig.update_layout(xaxis_title='Cluster', yaxis_title='Count')
    return fig

def segment_data():
    # data_path = r'C:\Users\ALBER\OneDrive\Desktop\Streamlit_docker_app\data\users.db'
    # model_path = r'Streamlit_app\Notebooks\best_clustering_model.pkl'
    # scaler_path = r'Streamlit_app\Notebooks\scaler.pkl'
    
    data_path = '/app/data/users.db'  # Correct Docker container path
    model_path = '/app/model/best_clustering_model.pkl'  # Correct Docker container path
    scaler_path = '/app/model/scaler.pkl'  # Correct Docker container path


    data = load_data_from_db(data_path)
    if data is not None and not data.empty:
        model = load_model(model_path)
        scaler = load_model(scaler_path)
        expected_features = ['age', 'annual_income', 'spending_score']
        if all(feature in data.columns for feature in expected_features):
            features = data[expected_features].values
            standardized_features = scaler.transform(features)
            data['Cluster'] = model.predict(standardized_features)
            return data
        else:
            missing_features = [feature for feature in expected_features if feature not in data.columns]
            st.error(f"Missing required features for prediction: {missing_features}")
            return None
    else:
        st.error("The database is empty. Please upload data first.")
        return None

def plot_feature_distribution(data, cluster):
    features = ['age', 'annual_income', 'spending_score']
    colors = ['tomato', 'gold', 'lightgreen']  # Different colors for each histogram
    fig = make_subplots(rows=1, cols=3, subplot_titles=features)
    for i, (feature, color) in enumerate(zip(features, colors)):
        fig.add_trace(
            go.Histogram(x=data[data['Cluster'] == cluster][feature], name=feature, marker_color=color),
            row=1, col=i+1
        )
    fig.update_layout(title_text=f'Distribution of Features for Cluster {cluster}', showlegend=False)
    return fig

def compare_all_clusters(data):
    features = ['age', 'annual_income', 'spending_score']
    clusters = data['Cluster'].unique()
    cols = len(clusters)

    # Create a subplot grid with a row for each feature
    fig = make_subplots(rows=len(features), cols=1, subplot_titles=[f'Distribution of {feature}' for feature in features])

    # Add box plots for each cluster in the respective feature row
    for i, feature in enumerate(features):
        for cluster in clusters:
            fig.add_trace(
                go.Box(
                    y=data[data['Cluster'] == cluster][feature],
                    name=f'Cluster {cluster}',
                    boxpoints='all',  # Optionally, show all points
                    jitter=0.5,       # Spread points out so they are not superimposed
                    marker_color=px.colors.qualitative.Plotly[i]  # Use Plotly's qualitative colors
                ),
                row=i+1, col=1
            )

    # Update layout to improve clarity and presentation
    fig.update_layout(
        title_text='Feature Distribution Across Clusters',
        height=900,
        showlegend=True,
        legend_title_text='Clusters'
    )
    return fig


def main():
    st.title("Worker's Data Segmentation Application")
    st.sidebar.title("Navigation")
    options = ["Home", "Upload and Segment", "Segment Existing Data", "Continuous Segmentation"]
    choice = st.sidebar.radio("Choose an option", options)

    if choice == "Home":
        st.subheader("Home")
        st.write("Welcome to the Workers' Data Segmentation Application. Choose an option from the sidebar to begin.")


    elif choice == "Upload and Segment":
        st.subheader("Upload CSV Data and Perform Segmentation")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file and st.button("Upload and Segment Data"):
            if insert_data_from_csv(r'C:\Users\ALBER\OneDrive\Desktop\Streamlit_docker_app\data\users.db', uploaded_file):
                st.success("Data successfully uploaded and will now be segmented.")
                data = segment_data()
                if data is not None:
                    fig = plot_clusters(data)
                    st.plotly_chart(fig)
                    
    elif choice == "Segment Existing Data":
        st.subheader("Perform Segmentation on Existing Data")
        data = segment_data()
        if data is not None:
            fig = plot_clusters(data)
            st.plotly_chart(fig)
            cluster_choice = st.selectbox("Choose a cluster to examine", options=sorted(data['Cluster'].unique()))
            feature_fig = plot_feature_distribution(data, cluster_choice)
            st.plotly_chart(feature_fig)
            if st.button("Compare All"):
                try:
                    comparison_fig = compare_all_clusters(data)
                    st.plotly_chart(comparison_fig)
                except Exception as e:
                    st.error(f"Failed to generate comparison: {str(e)}")
    elif choice == "Continuous Segmentation":
        st.subheader("Continuous Segmentation")
        container = st.empty()
        while True:
            data = segment_data()
            if data is not None:
                fig = plot_clusters(data)
                container.plotly_chart(fig)
            time.sleep(1)  # Wait for 1 second

if __name__ == "__main__":
    main()

