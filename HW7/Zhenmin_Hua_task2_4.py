from sentence_transformers import SentenceTransformer, util
import os
import csv
import time
import numpy as np
import pandas as pd

# model
model = SentenceTransformer('all-MiniLM-L6-v2')

# corpus_sentences
corpus = list(pd.read_csv('test.csv').text)
print('Corpus_len:', len(corpus))

print("Encode the corpus. This might take a while")
corpus_embeddings = model.encode(corpus, batch_size=64, show_progress_bar=True, convert_to_tensor=True)

print("Start clustering")
start_time = time.time()

#Two parameters to tune:
#min_cluster_size: Only consider cluster that have at least 25 elements
#threshold: Consider sentence pairs with a cosine-similarity larger than threshold as similar
clusters = util.community_detection(corpus_embeddings, min_community_size=15, threshold=0.75)

print("Clustering done after {:.2f} sec".format(time.time() - start_time))

#Print for all clusters the top 3 and bottom 3 elements
for i, cluster in enumerate(clusters):
    print("\nCluster {}, #{} Elements ".format(i+1, len(cluster)))

df['cluster'] = 51
for i in range(len(clusters)):
  for j in clusters[i]:
    df['cluster'][j] = i

from sklearn.metrics.cluster import normalized_mutual_info_score, adjusted_rand_score
print('normalized_mutual_info_score: ', normalized_mutual_info_score(df.category, df['cluster']))
print('adjusted_rand_score: ', adjusted_rand_score(df.category, df['cluster']))