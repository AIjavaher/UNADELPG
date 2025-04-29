from neo4j import GraphDatabase
from typing import Set, List, Dict
from collections import deque
from dataclasses import dataclass
import time

xx = 55

@dataclass
class PathInfo:
    nodes: List[int]  # Changed from List[str] to List[int]
    length: int

    def __hash__(self):
        return hash(tuple(self.nodes))

def find_next_destinations(driver, origin_id: int) -> Set[int]:  # Changed from str to int
    """
    Execute Neo4j query to find next possible destinations from the given origin_id
    """
    query = """
    MATCH (startGraph:FeatureGraph {id: $origin_id})-[]->(intLink1:InteriorFeatureLink)-[]-(abs1:AbstractLink)-[s1:STARTNODE]->(startNode)
    MATCH (startGraph:FeatureGraph {id: $origin_id})-[]->(intLink2:InteriorFeatureLink)-[]-(abs2:AbstractLink)-[s2:ENDNODE]->(endNode)
    WHERE startNode.type = 'exterior' AND endNode.type = 'exterior'
    OPTIONAL MATCH (int1:InteriorFeatureLink)-[]-(abs3:AbstractLink)-[r1:ENDNODE]->(startNode)
    OPTIONAL MATCH (int2:InteriorFeatureLink)-[]-(abs4:AbstractLink)-[r2:STARTNODE]->(endNode)
    OPTIONAL MATCH (f1:FeatureGraph)-[]->(int1)
    OPTIONAL MATCH (f2:FeatureGraph)-[]->(int2)
    RETURN DISTINCT f1.id as dest_id1, f2.id as dest_id2
    """
    with driver.session(database="waterpipes") as session:
        result = session.run(query, origin_id=origin_id)
        destinations = set()
        for record in result:
            if record["dest_id1"] is not None:  # Changed condition to handle None
                destinations.add(int(record["dest_id1"]))  # Convert to int
            if record["dest_id2"] is not None:  # Changed condition to handle None
                destinations.add(int(record["dest_id2"]))  # Convert to int
        return destinations

def find_all_paths_to_target(driver, start_id: int, target_id: int, max_depth: int = 50) -> List[PathInfo]:
    """
    Find all unique paths from start_id to target_id in the graph, keeping paths separate.
    """
    paths_in_progress = deque([PathInfo(nodes=[start_id], length=1)])
    completed_paths = []
    visited_combinations = set()

    while paths_in_progress:
        current_path_info = paths_in_progress.popleft()
        current_path = current_path_info.nodes
        current_node = current_path[-1]

        if len(current_path) > max_depth:
            continue

        next_destinations = find_next_destinations(driver, current_node)

        for next_node in next_destinations:
            if next_node in current_path:
                continue

            new_path = current_path + [next_node]
            path_key = tuple(new_path)

            if path_key in visited_combinations:
                continue
            visited_combinations.add(path_key)

            new_path_info = PathInfo(
                nodes=new_path,
                length=len(new_path)
            )

            if next_node == target_id:
                completed_paths.append(new_path_info)
            else:
                paths_in_progress.append(new_path_info)

    return completed_paths

def print_paths(paths: List[PathInfo]):
    """
    Print paths in a readable format with statistics
    """
    if not paths:
        print("No paths found!")
        return

    print(f"\nFound {len(paths)} unique paths:")
    paths.sort(key=lambda x: x.length)

    for i, path in enumerate(paths, 1):
        print(f"\nPath {i} (length {path.length}):")
        print(" -> ".join(str(node) for node in path.nodes))  # Convert nodes to strings when joining

# Example usage
if __name__ == "__main__":
    uri = "neo4j://localhost:7687"
    user = "neo4j"
    password = "12345678"
    driver = GraphDatabase.driver(uri, auth=(user, password))

    start_node = 2092        # Changed from string to int
    target_node = 3200  # Changed from string to int

    print(f"Finding paths from {start_node} to {target_node}...")
    start_time = time.time()
    paths = find_all_paths_to_target(driver, start_node, target_node)
    end_time = time.time()
    elapsed_time = end_time - start_time
    formatted_time = "{:.3f}".format(elapsed_time)
    print_paths(paths)
    print(f"\nThis process took {formatted_time} seconds.")
