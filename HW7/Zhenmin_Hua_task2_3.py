from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer, util, models
import random
import torch
import numpy as np
import os
import csv
import time
import numpy as np
import pandas as pd
import requests
import ampligraph
from ampligraph.datasets import load_from_csv
import warnings
warnings.filterwarnings("ignore")

# Model
model = SentenceTransformer('all-MiniLM-L6-v2')

# We donwload the Quora Duplicate Questions Dataset (https://www.quora.com/q/quoradata/First-Quora-Dataset-Release-Question-Pairs)
# and find similar question in it
url = "http://qim.fs.quoracdn.net/quora_duplicate_questions.tsv"
dataset_path = "quora_duplicate_questions.tsv"
max_corpus_size = 50000  # We limit our corpus to only the first 50k questions

# Download dataset if needed
if not os.path.exists(dataset_path):
    print("Download dataset")
    util.http_get(url, dataset_path)

# Get all unique sentences from the file
corpus_sentences = set()
with open(dataset_path, encoding='utf8') as fIn:
    reader = csv.DictReader(fIn, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        corpus_sentences.add(row['question1'])
        corpus_sentences.add(row['question2'])
        if len(corpus_sentences) >= max_corpus_size:
            break

corpus_sentences = list(corpus_sentences)

new_dimension = 128

random.shuffle(corpus_sentences)

#To determine the PCA matrix, we need some example sentence embeddings.
#Here, we compute the embeddings for 20k random sentences from the AllNLI dataset
pca_train_sentences = corpus_sentences[0:20000]
train_embeddings = model.encode(pca_train_sentences, convert_to_numpy=True)

#Compute PCA on the train embeddings matrix
pca = PCA(n_components=new_dimension)
pca.fit(train_embeddings)
pca_comp = np.asarray(pca.components_)

# We add a dense layer to the model, so that it will produce directly embeddings with the new size
dense = models.Dense(in_features=model.get_sentence_embedding_dimension(), out_features=new_dimension, bias=False, activation_function=torch.nn.Identity())
dense.linear.weight = torch.nn.Parameter(torch.tensor(pca_comp))
model.add_module('dense', dense)

print("Encode the corpus. This might take a while")
corpus_embeddings_pca = model.encode(corpus_sentences, batch_size=64, show_progress_bar=True, convert_to_tensor=True)

print("Start clustering")
start_time = time.time()

#Two parameters to tune:
#min_cluster_size: Only consider cluster that have at least 25 elements
#threshold: Consider sentence pairs with a cosine-similarity larger than threshold as similar
clusters_pca = util.community_detection(corpus_embeddings_pca, min_community_size=25, threshold=0.75)

print("Clustering done after {:.2f} sec".format(time.time() - start_time))

#Print for all clusters the top 3 and bottom 3 elements
for i, cluster in enumerate(clusters_pca):
    print("\nCluster {}, #{} Elements ".format(i+1, len(cluster)))


# kmean clustering
from sklearn.cluster import KMeans

start_time = time.time()

num_clusters = 5
clustering_model = KMeans(n_clusters=num_clusters)
clustering_model.fit(corpus_embeddings_pca)
cluster_assignment = clustering_model.labels_

clustered_sentences = [[] for i in range(num_clusters)]
for sentence_id, cluster_id in enumerate(cluster_assignment):
    clustered_sentences[cluster_id].append(corpus_sentences[sentence_id])

print("Clustering done after {:.2f} sec".format(time.time() - start_time))

for i, cluster in enumerate(clustered_sentences):
    print("Cluster ", i+1)
    print(cluster)
    print("")