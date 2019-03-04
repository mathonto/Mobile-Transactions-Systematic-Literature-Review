class Queries:
    def get_queries(self) -> []:
        with open('queries.txt') as file:
            queries = file.read().split('\n')
            return [query.replace(' ', '+') for query in queries]
