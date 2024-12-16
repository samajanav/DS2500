"""
DS2500
Homework 4
Janav Sama
Fall 2023

"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from collections import Counter

API_KEY = "5dd76d45f7ab4c4db888ef990b5900a9"

def extracting_data(API_KEY,URL):
    
    """
    A function to extract data using a given API key and URL, specifically 
    designed to retrieve information related to a specific keyword.
    """

    params = {
        "apiKey": API_KEY,
        "q": "Boeing"}
    
    response = requests.get(URL, params=params)
    
    data = {}
    data = response.json()
    
    return data

def extract_article_text(data):
    
    """
    A function to extract the text content from articles obtained through an
    API response, assuming the data structure includes a list of articles, 
    each with a "content" field.
    """
    
    articles = data.get("articles")
    article_texts = [article.get("content") for article in articles]
    
    return article_texts

def apply_tfidf(article_texts):
    
    """
    A function to apply the TF-IDF vectorization to a list of article texts, 
    returning the resulting TF-IDF matrix.
    """
    
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(article_texts)
    
    return tfidf_matrix

def apply_pca(tfidf_matrix, n_components=2):
    
    """
    A function to apply Principal Component Analysis (PCA) to reduce the 
    dimensionality of a TF-IDF matrix, with an option to specify the number of 
    components (default is 2). The function returns the transformed data after 
    PCA.
    """
    
    pca = PCA(n_components = n_components)
    data_pca = pca.fit_transform(tfidf_matrix.toarray())
    
    return data_pca

def perform_kmeans(data_pca, n_clusters = 5):
    
    """
    A function to perform k-means clustering on the given data after PCA 
    transformation, with an option to specify the number of clusters 
    (default is 5). The function returns the cluster labels assigned by 
    the k-means algorithm.
    """
    
    kmeans = KMeans (n_clusters = n_clusters)
    kmeans.fit(data_pca)
    
    labels = kmeans.labels_
    
    return labels


def analyze_clusters(data_pca, labels):
    
    """
    A function to analyze the clusters and plot the intertia graph.
    """

    inertia_values = []
    k_values = range(3, 11)
    
    for k in k_values:
        kmeans = KMeans(n_clusters = k, random_state = 0, n_init='auto')
        kmeans.fit(data_pca)
        inertia_values.append(kmeans.inertia_)

    first_article_pca_values = data_pca[0][:2]
    print("First two article's PCA values:", first_article_pca_values)

    cluster_counts = Counter(labels)
    print("Cluster count:", cluster_counts)

    plt.plot(k_values, inertia_values, marker='o')
    plt.title('Inertia vs. Number of Clusters')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('Inertia')
    plt.show()
    
def scatterplot_after_pca(data_pca, labels):
    
    """
    A function to create a scatterplot after applying PCA, with data points 
    colored according to their cluster labels obtained from k-means clustering.
    """
    
    df_pca = pd.DataFrame(data_pca, columns = ["PCA1", "PCA2"]) 
    df_pca["clusters"] = labels
    
    label_values = list(set(labels))
    
    for i in range(len(label_values)):
        cluster = df_pca[df_pca["clusters"] == i]
        plt.scatter(cluster["PCA1"],cluster["PCA2"],label = i)

    plt.title('Scatterplot After PCA with Cluster Colors')
    plt.xlabel('First Principal Component')
    plt.ylabel('Second Principal Component')
    plt.legend()
    plt.show()

def main():
    
    # Using the API
    data = extracting_data(API_KEY, "https://newsapi.org/v2/everything")
    
    # Extracting text content from articles
    article_texts = extract_article_text(data)

    # Applying TF-IDF
    tfidf_matrix = apply_tfidf(article_texts)

    # Applying PCA
    data_pca = apply_pca(tfidf_matrix, n_components = 2)

    # Performing K means and storing the labels 
    labels = perform_kmeans(data_pca, n_clusters = 5)
 
    # Problem 2,4 and Part 2 (Plot 1)
    analyze_clusters(data_pca, labels)
    
    # Part 2 (Plot 2)
    scatterplot_after_pca(data_pca, labels)


if __name__ == "__main__":
    main()
