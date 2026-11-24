from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        frontier = [(initial, 0)]
        best_depth = {initial.tiles: 0}
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            state, state_depth = frontier.pop()

            if state_depth > best_depth.get(state.tiles, state_depth):
                continue

            if state.is_goal:
                return SearchResult(
                    solution=state,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=state_depth,
                )

            if state_depth >= self.depth_limit:
                continue

            nodes_expanded += 1
            children = state.neighbors()
            for child in reversed(children):
                child_depth = state_depth + 1
                previous_depth = best_depth.get(child.tiles)
                if previous_depth is not None and previous_depth <= child_depth:
                    continue
                best_depth[child.tiles] = child_depth
                frontier.append((child, child_depth))
                nodes_generated += 1

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0,
        )
