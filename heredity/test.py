from heredity import *


family0 = {'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
           'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
           'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}}
one_gene0 = set()
two_genes0 = set()
have_trait0 = {'James'}


family1 = {'Arthur': {'name': 'Arthur', 'mother': None, 'father': None, 'trait': False},
           'Charlie': {'name': 'Charlie', 'mother': 'Molly', 'father': 'Arthur', 'trait': False},
           'Fred': {'name': 'Fred', 'mother': 'Molly', 'father': 'Arthur', 'trait': True},
           'Ginny': {'name': 'Ginny', 'mother': 'Molly', 'father': 'Arthur', 'trait': None},
           'Molly': {'name': 'Molly', 'mother': None, 'father': None, 'trait': False},
           'Ron': {'name': 'Ron', 'mother': 'Molly', 'father': 'Arthur', 'trait': None}}
one_gene1 = set()
two_genes1 = set()
have_trait1 = {'Fred'}


family2 = {'Arthur': {'name': 'Arthur', 'mother': None, 'father': None, 'trait': False},
           'Hermione': {'name': 'Hermione', 'mother': None, 'father': None, 'trait': False},
           'Molly': {'name': 'Molly', 'mother': None, 'father': None, 'trait': None},
           'Ron': {'name': 'Ron', 'mother': 'Molly', 'father': 'Arthur', 'trait': False},
           'Rose': {'name': 'Rose', 'mother': 'Ron', 'father': 'Hermione', 'trait': True}}
one_gene2 = set()
two_genes2 = set()
have_trait2 = {'Rose'}

print(joint_probability(family2, one_gene2, two_genes2, have_trait2))
