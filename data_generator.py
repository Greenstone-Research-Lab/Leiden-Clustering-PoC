import networkx as nx
import os

def generate_community_graph(output_path="data/synthetic_graph.graphml"):
    print("Generating synthetic graph...")
    
    # 5 different communities, with 40 nodes each.
    # Probability of connecting within a community is 40% (0.4), between communities is 5% (0.05)
    num_communities = 5
    nodes_per_community = 40
    p_in = 0.4
    p_out = 0.05
    
    # Generate the graph
    G = nx.planted_partition_graph(num_communities, nodes_per_community, p_in, p_out)
    
    print(f"Graph generated! Total Nodes: {G.number_of_nodes()}, Total Edges: {G.number_of_edges()}")
    
    # --- BUG FIX: Clean up complex data types for GraphML ---
    # Convert graph-level attributes (like 'partition' lists/sets) to strings
    for key, value in G.graph.items():
        if isinstance(value, (list, set, tuple, dict)):
            G.graph[key] = str(value)
            
    # Convert node attributes to strings if they are lists/sets
    for node, data in G.nodes(data=True):
        for key, value in data.items():
            if isinstance(value, (list, set, tuple, dict)):
                data[key] = str(value)
                
    # Convert edge attributes to strings if they are lists/sets
    for u, v, data in G.edges(data=True):
        for key, value in data.items():
            if isinstance(value, (list, set, tuple, dict)):
                data[key] = str(value)
    # --------------------------------------------------------

    # Create 'data' directory (if it doesn't exist)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the graph in GraphML format
    nx.write_graphml(G, output_path)
    print(f"Graph successfully saved to '{output_path}'.")

if __name__ == "__main__":
    generate_community_graph()