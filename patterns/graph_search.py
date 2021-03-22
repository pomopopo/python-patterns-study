#!/usr/local/bin/python3
"""
*图搜索
DFS = 深度优先(Depth First Search). 不撞南墙不回头, 能够快速找到一条路径,
但通常不是最优路径. DFS 用栈来存放数据.

BFS = 广度优先(Breadth First Search). 呈波浪状推进, 以时间换空间,
能找到最优解, 为能够波浪状搜索, 采用队列(Queue)作为 openlist 的数据结构.
大量的入队 / 出队, 就慢很多.

*本例:
有向图(a,b,c ...h) 如下:
   a ----> b
    \     / \
     \   /   \
      v v     v
f ---> c <---> d
^      |\
|      | \
|      v  \
e <--- g   h

ps 这里的例子特别简略, 只能算是示意. 用于有权重路径的算法, 需要用 GBFS, Dijkstra, A*
等其他启发式搜索算法.
"""


class GraphSearch:
    def __init__(self, graph):
        self.graph = graph

    def find_path_dfs(self, start, end, path=None):
        path = path or []
        path.append(start)

        if start == end:
            return path

        for node in self.graph.get(start, []):
            if node not in path:
                newpath = self.find_path_dfs(node, end, path[:])
                if newpath:
                    return newpath

    def find_all_paths_dfs(self, start, end, path=None):
        path = path or []
        path.append(start)

        if start == end:
            return [path]

        paths = []
        for node in self.graph.get(start, []):
            if node not in path:
                newpaths = self.find_all_paths_dfs(node, end, path[:])
                paths.extend(newpaths)
        return paths

    def find_shortest_path_dfs(self, start, end, path=None):
        path = path or []
        path.append(start)

        if start == end:
            return path

        shortest = None
        for node in self.graph.get(start, []):
            if node not in path:
                newpath = self.find_shortest_path_dfs(node, end, path[:])
                if newpath and (not shortest or len(newpath) < len(shortest)):
                    shortest = newpath
        return shortest

    def find_shortest_path_bfs(self, start, end):
        queue = [start]
        dist_to = {start: 0}
        edge_to = {}

        if start == end:
            return queue

        while len(queue):
            value = queue.pop(0)
            for node in self.graph[value]:
                if node not in dist_to:  #dist_to s  dist_to.keys() 的简写
                    edge_to[node] = value
                    dist_to[node] = dist_to[value] + 1
                    queue.append(node)
                    if end in edge_to:
                        path = []
                        node = end
                        while dist_to[node] != 0:
                            path.insert(0, node)
                            node = edge_to[node]
                        path.insert(0, start)
                        return path


def main():
    """
    >>> graph = {
    ...     'a': ['b', 'c'],
    ...     'b': ['c', 'd'],
    ...     'c': ['d', 'g'],
    ...     'd': ['c'],
    ...     'e': ['f'],
    ...     'f': ['c'],
    ...     'g': ['e'],
    ...     'h': ['c'],
    ... }

    >>> graph_search = GraphSearch(graph)

    # DFS
    >>> graph_search.find_path_dfs('a','d')
    ['a', 'b', 'c', 'd']
    >>> graph_search.find_path_dfs('g','f')
    ['g', 'e', 'f']

    >>> graph_search.find_path_dfs('c','h')

    >>> graph_search.find_path_dfs('c','x')


    # ALL PATH DFS
    >>> graph_search.find_all_paths_dfs('a','d')
    [['a', 'b', 'c', 'd'], ['a', 'b', 'd'], ['a', 'c', 'd']]

    # SHORTEST DFS
    >>> graph_search.find_shortest_path_dfs('a','d')
    ['a', 'b', 'd']
    >>> graph_search.find_shortest_path_dfs('a','f')
    ['a', 'c', 'g', 'e', 'f']

    # SHORTEST BFS
    >>> graph_search.find_shortest_path_bfs('a','d')
    ['a', 'b', 'd']
    >>> graph_search.find_shortest_path_bfs('a','f')
    ['a', 'c', 'g', 'e', 'f']
    >>> graph_search.find_shortest_path_bfs('g','f')
    ['g', 'e', 'f']
    >>> graph_search.find_shortest_path_bfs('a','h')

    >>> graph_search.find_shortest_path_bfs('a','x')

    """


if __name__ == "__main__":
    # main()
    import doctest
    doctest.testmod(verbose=True)
