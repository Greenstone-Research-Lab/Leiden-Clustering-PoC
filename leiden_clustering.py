import networkx as nx
import igraph as ig
import leidenalg
import matplotlib.pyplot as plt

def run_leiden_clustering(input_path="data/synthetic_graph.graphml", output_img="data/leiden_communities.png"):
    print(f"Loading graph from '{input_path}'...")
    
    # 1. Read the GraphML file using NetworkX
    G_nx = nx.read_graphml(input_path)
    print(f"Graph loaded successfully. Nodes: {G_nx.number_of_nodes()}, Edges: {G_nx.number_of_edges()}")
    
    # 2. Convert NetworkX graph to iGraph format for high-speed Leiden execution
    print("Converting NetworkX graph to iGraph format...")
    G_ig = ig.Graph.from_networkx(G_nx)
    
    # 3. Run the Leiden Algorithm
    # We use ModularityVertexPartition which optimizes the modularity score
    print("Running Leiden algorithm for community detection...")
    partition = leidenalg.find_partition(G_ig, leidenalg.ModularityVertexPartition)
    
    # partition.membership contains the community ID for each node
    communities = partition.membership
    num_communities = len(set(communities))
    print(f"Algorithm finished! Detected {num_communities} distinct communities.")
    
    # 4. Prepare for Visualization
    print("Preparing visualization...")
    # Map the community IDs as colors for our NetworkX nodes
    color_map = []
    for i in range(len(G_nx.nodes())):
        # The index in iGraph perfectly matches the order of nodes in NetworkX's node list
        color_map.append(communities[i])
        
    plt.figure(figsize=(12, 8))
    
    # spring_layout groups heavily connected nodes closer together visually
    pos = nx.spring_layout(G_nx, seed=42) 
    
    # Draw the graph
    nx.draw_networkx_nodes(G_nx, pos, node_color=color_map, cmap=plt.cm.tab20, node_size=150, alpha=0.9)
    nx.draw_networkx_edges(G_nx, pos, alpha=0.3)
    
    plt.title("Leiden Clustering Algorithm - Community Detection", fontsize=16)
    plt.axis('off') # Hide axes for a cleaner look
    
    # 5. Save and Show the result
    plt.savefig(output_img, dpi=300, bbox_inches='tight')
    print(f"High-resolution cluster map saved to '{output_img}'.")
    plt.show()

if __name__ == "__main__":
    run_leiden_clustering()