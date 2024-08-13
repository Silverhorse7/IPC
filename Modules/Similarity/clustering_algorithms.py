from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import matplotlib.pyplot as plt
import numpy as np

# Perform K-means clustering
def run_kmeans_clustering(embedding, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters)
    labels = kmeans.fit_predict(embedding)
    return labels

# Perform Agglomerative clustering
def run_agglomerative_clustering(embedding, n_clusters):
    agglomerative = AgglomerativeClustering(n_clusters=n_clusters)
    labels = agglomerative.fit_predict(embedding)
    return labels

# Calculate silhouette score
def calculate_silhouette_score(embedding, labels):
    score = silhouette_score(embedding, labels)
    return score

# Calculate davies bouldin score
def calculate_davies_bouldin_score(embedding, labels):
    score = davies_bouldin_score(embedding, labels)
    return score

# Calculate calinski harabasz score
def calculate_calinski_harabasz_score(embedding, labels):
    score = calinski_harabasz_score(embedding, labels)
    return score

# Find optimal k using different evaluation metrics
def find_optimal_k(embedding, clustering_algo, max_k=100):
    silhouette_scores = []
    davies_bouldin_scores = []
    calinski_harabasz_scores = []

    for k in range(5, max_k + 1):
        if clustering_algo == 'kmeans':
            labels = run_kmeans_clustering(embedding, k)
        elif clustering_algo == 'agglomerative':
            labels = run_agglomerative_clustering(embedding, k)
        else:
            raise ValueError("Invalid clustering algorithm. Choose 'kmeans' or 'agglomerative'.")

        silhouette_scores.append(silhouette_score(embedding, labels))
        davies_bouldin_scores.append(davies_bouldin_score(embedding.toarray(), labels))
        calinski_harabasz_scores.append(calinski_harabasz_score(embedding.toarray(), labels))

    optimal_k_silhouette = np.argmax(silhouette_scores) + 5
    optimal_k_davies_bouldin = np.argmin(davies_bouldin_scores) + 5
    optimal_k_calinski_harabasz = np.argmax(calinski_harabasz_scores) + 5

    return (optimal_k_silhouette, silhouette_scores), (optimal_k_davies_bouldin, davies_bouldin_scores), (optimal_k_calinski_harabasz, calinski_harabasz_scores)

def elbow_method(embedding, max_k=100):
    ssd = []
    for k in range(5, max_k + 1):
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(embedding)
        ssd.append(kmeans.inertia_)
    return ssd

def plot_elbow(ssd, embedding_name):
    plt.plot(range(5, len(ssd) + 5), ssd, marker='o')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Sum of Squared Distances')
    plt.title('Elbow Method for ' + embedding_name)
    plt.show()

def plot_scores(scores, score_name, embedding_name):
    plt.plot(range(5, len(scores) + 5), scores, marker='o')
    plt.xlabel('Number of Clusters')
    plt.ylabel(score_name)
    plt.title(score_name + ' for ' + embedding_name)
    plt.show()