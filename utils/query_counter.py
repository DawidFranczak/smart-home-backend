from django.db import connection


def query_counter(func):
    """
    Decorator to count the number of queries executed by a function.
    """

    def wrapper(*args, **kwargs):
        # Reset the query count before executing the function
        connection.queries.clear()
        query_count_b = len(connection.queries)
        result = func(*args, **kwargs)
        # Count the number of queries executed
        query_count = len(connection.queries)
        print(f"Number of queries executed: {query_count-query_count_b}")
        return result

    return wrapper
