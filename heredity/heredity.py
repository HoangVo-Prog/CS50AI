import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue
        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    tracking_dictionary = {
        person: [
            2 if person in two_genes else 1 if person in one_gene else 0,
            True if person in have_trait else False
        ]
        for person in people.keys()
    }

    parents = [person for person, info in people.items() if info['mother'] is None]
    children = [person for person in people.keys() if person not in parents]

    joint_prob = 1
    for person in parents:
        parent_prob = (
            (PROBS["gene"][tracking_dictionary[person][0]]) *
            (PROBS["trait"][tracking_dictionary[person][0]][tracking_dictionary[person][1]])
        )
        print(parent_prob)
        joint_prob *= parent_prob

    # Those probs below belong to case gene 0, 1, 2
    prob_genes = {
        0: {True: 0.01, False: 0.99},
        1: {True: 0.495, False: 0.505},  # True means pass 1 gene, False means no pass
        2: {True: 0.99, False: 0.01}
    }

    combinations = [[False, False], [False, True], [True, False], [True, True]]
    for person in children:
        children_parents = list()
        children_parents.append(people[person]["mother"])
        children_parents.append(people[person]["father"])
        current_probability = 0
        gene = tracking_dictionary[person][0]
        for case in combinations:
            value1 = 1 if case[0] else 0
            value2 = 1 if case[1] else 0
            if value1 + value2 == gene:
                current_probability += (prob_genes[tracking_dictionary[children_parents[0]][0]][case[0]] *
                                        prob_genes[tracking_dictionary[children_parents[1]][0]][case[1]])
        # print(person, current_probability)
        joint_prob *= ((1 if current_probability == 0 else current_probability) *
                       PROBS["trait"][tracking_dictionary[person][0]][tracking_dictionary[person][1]])

    return joint_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in one_gene:
        probabilities[person]["gene"][1] += p

    for person in two_genes:
        probabilities[person]["gene"][2] += p

    for person in probabilities:
        if person not in one_gene and person not in two_genes:
            probabilities[person]["gene"][0] += p

    for person in have_trait:
        probabilities[person]["trait"][True] += p

    for person in probabilities:
        if person not in have_trait:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities.keys():

        sum_gene = sum(probabilities[person]["gene"].values())
        sum_trait = sum(probabilities[person]["trait"].values())

        for gene in probabilities[person]["gene"].keys():
            probabilities[person]["gene"][gene] /= sum_gene

        for trait in probabilities[person]["trait"].keys():
            if sum_trait == 0:
                probabilities[person]["trait"][False] = 1
            else:
                probabilities[person]["trait"][trait] /= sum_trait


if __name__ == "__main__":
    main()
