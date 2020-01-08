from collections import Counter, defaultdict


def get_statement_counts(indexed_concepts):
    by_window_size = {}
    for window_size in indexed_concepts:
        by_window_size[window_size] =\
            Counter(indexed_concepts[window_size])

    return by_window_size

def get_min(counts_a, counts_b, minimum_window_size):
    minimum_counts_per_window_size = defaultdict(int)

    for window_size in range(1, minimum_window_size+1):
        for common_statement in counts_a[window_size].keys() &\
                                counts_b[window_size].keys():
            minimum_counts_per_window_size[window_size] +=\
                min(counts_a[window_size][common_statement],
                    counts_b[window_size][common_statement])

    return minimum_counts_per_window_size


def get_difference(counts_a, counts_b, maximum_window_size):
    difference_per_window_size = defaultdict(int)

    for window_size in range(1, maximum_window_size+1):
        # we process common keys and then just add in unique keys
        if window_size in counts_a.keys() and\
            window_size in counts_b.keys():
            for common_statement in counts_a[window_size].keys() &\
                                    counts_b[window_size].keys():
                difference_per_window_size[window_size] +=\
                    counts_a[window_size][common_statement] -\
                        counts_b[window_size][common_statement]

            for a_statement in counts_a[window_size].keys() -\
                                counts_b[window_size].keys():
                difference_per_window_size[window_size] +=\
                    counts_a[window_size][a_statement]

            for b_statement in counts_b[window_size].keys() -\
                                counts_a[window_size].keys():
                difference_per_window_size[window_size] +=\
                    counts_b[window_size][b_statement]

        if window_size in counts_a.keys() and\
            window_size not in counts_b.keys():
            # we just add in all the values at this window size
            difference_per_window_size[window_size] +=\
                sum(counts_a[window_size].values())

        if window_size in counts_b.keys() and\
            window_size not in counts_a.keys():
            difference_per_window_size[window_size] +=\
                sum(counts_b[window_size].values())

    return difference_per_window_size


def sinreich_relationship_similarity_measure(statements_a, statements_b):
    """
    D. Sinreich et al.

    Mental models as a practical tool in the engineer's toolbox,
    International Journal of Production Research · July 2005
    DOI: 10.1080/00207540500057373

    See equations (2) - (6), take w_k, w_l as 1 and f^i_kl a statement,
    a concept pair.
    """

    smaller_window_size = min(len(statements_a), len(statements_b))
    maximum_window_size = max(len(statements_a), len(statements_b))

    counts_a = get_statement_counts(statements_a)
    counts_b = get_statement_counts(statements_b)

    common_arc = get_min(counts_a, counts_b, smaller_window_size)
    exclusive_arc = get_difference(counts_a, counts_b, maximum_window_size)

    relationship_similarity = {}

    prior_common_arc = 0
    prior_exclusive_arc = 0
    for window_size in range(1, maximum_window_size+1):
        common_arc_at_window_size = 0
        exclusive_arc_at_window_size = exclusive_arc[window_size]
        if window_size in common_arc:
            common_arc_at_window_size = common_arc[window_size]

        relationship_similarity[window_size] = 0

        denominator =\
            (prior_common_arc + common_arc_at_window_size +
                prior_exclusive_arc + exclusive_arc_at_window_size)

        if denominator != 0:
            relationship_similarity[window_size] =\
                (prior_common_arc + common_arc_at_window_size) /\
                denominator

        prior_common_arc += common_arc_at_window_size
        prior_exclusive_arc += exclusive_arc_at_window_size

    return relationship_similarity
