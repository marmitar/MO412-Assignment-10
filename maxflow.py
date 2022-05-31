"""Find maximum flow in 'links.csv'."""

# Python 3.10+ required
from enum import Enum, auto, unique
import networkx as nx
import os.path
from typing import Any, BinaryIO, TextIO


def path_to(filename: str):
    """Relative path to `filename` from current 'maxflow.py' file."""
    try:
        program = __file__
    # some environemnts (like bpython) don't define '__file__',
    # so we assume that the file is in the current directory
    except NameError:
        return filename

    basedir = os.path.dirname(program)
    fullpath = os.path.join(basedir, filename)
    return os.path.relpath(fullpath)


def read_graph(*, links: str | TextIO = path_to('links.csv')) -> nx.DiGraph:
    """Read nodes and links from the provided file."""
    return nx.read_edgelist(links, delimiter=',', create_using=nx.DiGraph, data=(('cost',int),))


def max_flow(graph: nx.DiGraph, /, *, source: str, sink: str) -> int:
    return 0


def draw_graph(graph: nx.DiGraph, /, output: BinaryIO | None = None):
    """Draw graph and its components using Matplotlib."""
    from matplotlib import pyplot as plt

    nx.draw(graph, node_size=1000, font_size=10)

    if output is None:
        plt.show(block=True)
    else:
        plt.savefig(output)


@unique
class OutputMode(Enum):
    NO_OUTPUT = 'NO OUTPUT'
    SHOW_OUTPUT = 'SHOW'


class Arguments:
    number: bool = False
    draw: BinaryIO | OutputMode


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    # arguments
    parser = ArgumentParser('maxflow.py')
    parser.add_argument('-d', '--draw', metavar='OUTPUT', nargs='?',
        type=FileType(mode='wb'), default=OutputMode.NO_OUTPUT, const=OutputMode.SHOW_OUTPUT,
        help=('Draw NetworkX graph to OUTPUT using Matplotlib. If no argument is provided,'
            ' the graph is drawn on a new window.'))

    args = parser.parse_args(namespace=Arguments)

    # reading input
    graph = read_graph()

    # maximum flow
    flow = max_flow(graph, source='Ti', sink='Iu')
    print(flow)

    # rendering with matplolib
    match args.draw:
        case OutputMode.NO_OUTPUT:
            pass
        case OutputMode.SHOW_OUTPUT:
            draw_graph(graph)
        case output_file:
            draw_graph(graph, output=output_file)
