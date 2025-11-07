from collections import Counter

from typing import List, Set, Tuple


def parse_query_no_stop_words(user_query: str,
                              stop_words: Set[str]) -> Set[str]:
    user_query = set(user_query.lower().split())
    relevant_words = user_query.difference(stop_words)
    return relevant_words


def match_document(document_words: Set[str], query_words: Set[str]) -> int:
    return len(document_words.intersection(query_words))


def parse_stop_words(filename: str) -> Set[str]:
    with open(filename, "r", encoding="utf-8") as file:
        stop_words = file.read().strip()
    return set(stop_words.lower().split(", "))


def find_documents(documents: List[Tuple[int, Set[str]]], stop_words:
                   Set[str], user_query: str) -> List[Tuple[int, int]]:
    query_no_stop_words = parse_query_no_stop_words(user_query, stop_words)
    result = []

    for film_id, document in documents:
        relevance = match_document(document, query_no_stop_words)
        if relevance > 0:
            result.append((film_id, relevance))
    return result


def films_rating(query_film_ids: List[str]) -> List[Tuple[int, int]]:
    film_ids = []
    for response in query_film_ids:
        response_ids = [
            int(id) for id in response.strip('[]').split(', ') if id.strip()
        ]
        film_ids.extend(response_ids)

    film_counts = Counter(film_ids)
    sorted_film_counts = film_counts.most_common()

    return sorted_film_counts


def rating_query_users(queries: List[str]) -> None:
    query_counts = Counter(queries)
    sorted_queries = query_counts.most_common()

    for query, count in sorted_queries:
        print(f"Запрос: {query}, Повторения: {count}")
