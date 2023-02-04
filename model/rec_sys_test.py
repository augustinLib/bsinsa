import pickle
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

with open('recsys/model/modelfile/final_embeddings.pickle', 'rb') as f:
        final_embedding = pickle.load(f)

dist_mtx = euclidean_distances(final_embedding, final_embedding)

np.save("data/data_sample/dist-mtx", dist_mtx)
data = np.load('data/data_sample/dist_mtx.npy')

import pandas as pd

df = pd.read_csv('data/data_sample/to_Dataloader.csv')
df2 = pd.read_csv('data/data_sample/dataframe/total_modified.csv')