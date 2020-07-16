def probability_function(n, m):
    """
    Calculates the probability, using the provided formula:
    P = 1 - [n * ((n-1)/n)^m - n * (1/n)^m]
    Where:
        - n: is the number of possible cypher functions.
        - m: number of times the Oracle has been executed.
        - P: probability of getting all the possible cyphers under
             the n functions.
    """
    return 1 - (n * pow((n-1)/n, m) - n * pow(1/n, m))


def min_elements(n, required_probability):
    """
    Simple greedy algorithm that finds the minimum number of tries an
    attacker would need to get all the possible cypher-texts under all
    :n: possible functions, with a probability of :required_probability:
    """
    current_probability = 0
    i = 0
    while current_probability <= required_probability:
        i += 1
        current_probability = probability_function(n, i)
    return i


elements_number = 10
probability = 0.99

print(f"Minimum number of tries with {elements_number} functions to get"
      f" a {probability} probability: {min_elements(10, 0.99)} tries.")
