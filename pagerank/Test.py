from pagerank import *


corpus1 = {'1': {'2'}, '2': {'3', '1'}, '3': {'4', '2', '5'}, '4': {'2', '1'}, '5': set()}
corpus2 = {'1': {'2'}, '2': {'3', '1'}, '3': {'5', '4', '2'}, '4': {'1', '2'}, '5': set()}
corpus3 = {'1': {'2'}, '2': {'3', '1'}, '3': {'5', '4', '2'}, '4': {'1', '2'}, '5': set()}


corpus = corpus1
a = sample_pagerank(corpus, 0.85, 10000)
b = iterate_pagerank(corpus, 0.85)

print(a)

print(b)


