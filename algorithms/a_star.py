import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan dos blocos até suas posições finais."""
        distance = 0
        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            goal_index = tile - 1
            row, column = divmod(index, 3)
            goal_row, goal_column = divmod(goal_index, 3)
            distance += abs(row - goal_row) + abs(column - goal_column)
        return distance

    def search(self, initial: State) -> SearchResult:
        counter = 0
        initial_g = initial.cost
        frontier = [(initial_g + self.heuristic(initial), counter, initial)]
        best_cost = {initial.tiles: initial_g}
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            _, _, state = heapq.heappop(frontier)
            state_cost = best_cost.get(state.tiles)
            if state_cost is None or state.cost != state_cost:
                continue

            if state.is_goal:
                return SearchResult(
                    solution=state,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=len(state.path()) - 1,
                )

            nodes_expanded += 1
            for child in state.neighbors():
                previous_cost = best_cost.get(child.tiles)
                if previous_cost is not None and child.cost >= previous_cost:
                    continue

                best_cost[child.tiles] = child.cost
                counter += 1
                priority = child.cost + self.heuristic(child)
                heapq.heappush(frontier, (priority, counter, child))
                nodes_generated += 1

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0,
        )
