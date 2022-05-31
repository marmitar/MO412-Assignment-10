"""Find maximum flow in 'links.csv'."""
import os.path
import networkx as nx


def path_to(filename: str):
    """Relative path to `filename` from current 'maxflow.py' file."""
    try:
        basedir = os.path.dirname(__file__)
        fullpath = os.path.join(basedir, filename)
        return fullpath
    # some environemnts (like bpython) don't define '__file__',
    # so we assume that the file is in the current directory
    except NameError:
        return filename


def read_graph(*, links: str = path_to('links.csv')) -> nx.DiGraph:
    """Read nodes and links from the provided file."""
    return nx.read_edgelist(links, delimiter=',', create_using=nx.DiGraph, data=(('capacity', int),))


def max_flow(graph: nx.DiGraph, source: str, sink: str) -> int:
    """Find the maximum flow from `source` to `sink` in `graph`."""
    flow, _ = nx.maximum_flow(graph, source, sink)
    return flow


def default_color(n: int):
    """Get the `n`th color from the default Matplotlib cycler."""
    from matplotlib import rcParams

    # from https://matplotlib.org/stable/gallery/color/color_cycle_default.html
    prop_cycle = rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']

    for idx, color in enumerate(colors):
        if idx >= n:
            return color
    return 'blue'


def draw_graph(graph: nx.DiGraph, source: str, sink: str):
    """Draw graph and its components using Matplotlib."""
    from matplotlib import pyplot as plt  # matplotlib is only required for drawing

    # node position (Kamada-Kawai requires SciPy)
    try:
        position = nx.kamada_kawai_layout(graph)
    except ModuleNotFoundError:
        position = None

    # node & color
    colordict = {source: default_color(2), sink: default_color(1)}
    colors = tuple(colordict.get(node, default_color(0)) for node in graph.nodes)
    nx.draw(graph, position, node_color=colors, with_labels=True, node_size=1000, font_size=10)

    # edges
    capacity = {(u,v): c for u,v,c in graph.edges.data('capacity')}
    nx.draw_networkx_edge_labels(graph, position, edge_labels=capacity)

    # draw on a new window
    plt.show(block=True)


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    # arguments
    parser = ArgumentParser('maxflow.py')
    parser.add_argument('-d', '--draw', action='store_true',
        help='draw NetworkX graph using Matplotlib')

    args = parser.parse_args()

    # reading input
    graph = read_graph()
    source, sink = 'Ti', 'Iu'

    # maximum flow
    flow = max_flow(graph, source, sink)
    print(f'Maximum Flow from {source} to {sink}:', flow)

    # rendering with matplolib
    if args.draw:
        draw_graph(graph, source, sink)
