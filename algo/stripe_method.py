from models import Graph, Point


def stripe(g: Graph, dot: Point):
    separators = sorted(set(map(lambda x: x[1], g.vertices)))
    separators = [float('-inf')] + separators + [float('inf')]
    stripes = []
    for separ in range(len(separators) - 1):
        stripes.append((separators[separ], separators[separ + 1]))
    yield stripes
    table = first_stage(stripes, g)
    yield table
    stripe = find_stripe(stripes, dot)
    yield stripe
    edges_to_check = table[stripe]
    yield check_edges(edges_to_check, dot)


def edge_in_stripe(self, stripe):
    return (
        self.v1.point.y <= stripe[0] and self.v2.point.y >= stripe[1] or
        self.v2.point.y <= stripe[0] and self.v1.point.y >= stripe[1]
    )


def position_dot_edge(dot, edge):
    x1, y1 = edge.v1.point.coords
    x2, y2 = edge.v2.point.coords
    x3, y3 = dot.coords

    return (x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)


def first_stage(stripes, g: Graph):
    ans = {}
    for stripe in stripes:
        ans.update(
            {stripe: list(filter(
                lambda x: edge_in_stripe(x, stripe), g.edges
                ))})
    return ans


def dot_in_stripe(dot, stripe):
    return stripe[0] < dot.y <= stripe[1]


def find_stripe(stripes, dot):
    return filter(lambda x: dot_in_stripe(dot, x), stripes).__next__()


def dot_between_edges(dot, edges):
    return (
        position_dot_edge(dot, edges[0]) *
        position_dot_edge(dot, edges[1]) < 0
    )


def check_edges(edges, dot):
    tuples = []
    for edge in range(len(edges) - 1):
        tuples.append((edges[edge], edges[edge + 1]))
    ans = filter(lambda x: dot_between_edges(dot, x), tuples).__next__()
    return list(ans)