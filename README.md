# UNADELPG
A Labelled Property Graph (LPG) model developed for the CityGML Utility Network ADE. Includes transformation rules, graph structure guidelines, and sample data scripts implemented in Neo4j for spatial querying and utility network analysis.

# UNADELPG - IFC to Graph rules

**UNADELPG** is a Python-based tool for constructing a **Labelled Property Graph (LPG)** representation of utility networks using **CityGML Utility Network ADE** concepts, implemented in **Neo4j**.

This code reads water pipeline network data from a CSV file and generates nodes and relationships according to a spatial and semantic graph model. The graph model is designed to support efficient **spatial querying**, **topological reasoning**, and **network analysis**.

---

## Features

- Converts water utility network datasets into a Labelled Property Graph structure.
- Models CityGML Utility Network ADE feature types (e.g., FeatureGraph, AbstractNetworkFeature).
- Creates nodes for spatial geometry points, pipeline segments, and associated metadata.
- Preserves semantic relationships such as STARTNODE, ENDNODE, and network hierarchy.
- Enables spatial analysis and pathfinding using Neo4j.

---

## Requirements

- Python 3.8+
- pandas
- neo4j Python driver
- Neo4j Desktop or Server (tested with Bolt connection)

---

## Usage

1. Update the CSV file path and Neo4j connection details in the script.
2. Prepare a Neo4j database (e.g., named `waterpipes`).
3. Run the script to import nodes and relationships into Neo4j.

The generated graph follows a normalised LPG structure optimised for spatial querying and connectivity analysis.

---

## Project Context

This repository supports the manuscript:

**"A Normalised Graph Model for Geospatial Utility Network Analysis Based on CityGML"**  
submitted to *Computers & Geosciences*.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

- Neo4j graph database platform
- CityGML Utility Network ADE framework
- Data courtesy of South East Water (case study: Frankston, Victoria, Australia)


---

## Pathfinding and Spatial Connectivity Analysis

This repository also includes a Python script for conducting **spatial pathfinding analysis** on the LPG-based utility network. The approach identifies all unique paths between a specified origin and target node within a defined depth limit.

### Features

- Computes all simple paths between two `FeatureGraph` nodes
- Traverses shared `InteriorFeatureLink` and `AbstractLink` nodes
- Avoids cycles and redundant paths using a visited-path cache
- Returns all paths and their lengths for statistical or visual analysis

### Method Overview

1. Uses Cypher queries to identify `FeatureGraph` connections through shared exterior nodes
2. Performs a **breadth-first search** with maximum depth control
3. Outputs paths as ordered node sequences, sorted by length
4. Provides timing information to evaluate performance

### Example Usage

```python
start_node = 2092
target_node = 3200
paths = find_all_paths_to_target(driver, start_node, target_node)
print_paths(paths)

