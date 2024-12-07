import numpy as np
from sklearn.decomposition import PCA
import random
from scipy.stats import mannwhitneyu

def estimate_global_dimension_pca(data,threshold): #threshold like 0.95
    pca = PCA()
    pca.fit(data)
    explained_variance = np.cumsum(pca.explained_variance_ratio_)
    global_dimension = np.argmax(explained_variance >= threshold) + 1
    return global_dimension

def dictionary_random_reducer(data, seed, N):
  
    dic_length= len(list(data.keys()))
    if N > dic_length:
        raise ValueError("N must be less than or equal to the number of items in the dictionary")

    random.seed(seed)
    lst = [1] * N + [0] * (dic_length - N)
    random.shuffle(lst)

    dicc= {}
    for i,key in enumerate(data.keys()):
        if lst[i]==1:
            dicc[key]= data[key]

    return dicc

def mannwhitneyu_stat(group1,group2):
# Mann-Whitney U test
    stat, p = mannwhitneyu(group1, group2)
    #print('Mann-Whitney U Test: Statistic=%.3f, p=%.3f' % (stat, p))

    # if p > 0.05:
    #     print('Probably the same distribution (fail to reject H0)')
    # else:
    #     print('Probably different distributions (reject H0)')
    return p