from pyvis.network import Network
import networkx as nx
from community import community_louvain
import matplotlib.pyplot as plt
import json

# Load Json Triplets
def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)
triplets_path =  "../data/triplets.json"
triplets = load_json(triplets_path)

# breakpoint()
# Step 1: Build the graph
G = nx.Graph()

# Add triplets to the graph
for neighborhood in triplets['neighborhoods']:
    for document in neighborhood['triplets']['documents']:
        for triplet in document['triplets']:
            G.add_edge(triplet["entity_1"], triplet["entity_2"], relation=triplet["relation"])


#######Graph Analysis###############
# Compute the connected components of the graph
connected_components = list(nx.connected_components(G))

# Sort components by size (number of nodes)
sorted_components = sorted(connected_components, key=len, reverse=True)


# Analyze each connected graph
graph_info = []
for component in sorted_components:
    subgraph = G.subgraph(component)
    graph_info.append({
        "nodes": len(subgraph.nodes),
        "edges": len(subgraph.edges)
    })
print(graph_info)
    
# # Analyze the largest and second largest connected components
# largest_component = sorted_components[0]
# second_largest_component = sorted_components[1] if len(sorted_components) > 1 else set()

# # Get node and edge counts
# largest_nodes = len(largest_component)
# largest_edges = G.subgraph(largest_component).number_of_edges()

# second_largest_nodes = len(second_largest_component)
# second_largest_edges = G.subgraph(second_largest_component).number_of_edges()

# # Total counts for the entire graph
# total_nodes = G.number_of_nodes()
# total_edges = G.number_of_edges()

# print(largest_nodes, largest_edges, second_largest_nodes, second_largest_edges, total_nodes, total_edges)
#######Graph Analysis End###############



# find the largest connected subgraph
largest_connected_component = max(nx.connected_components(G), key=len)
G = G.subgraph(largest_connected_component)



# Step 2: Force Louvain to find 2 partitions
# Limit the number of communities to 2
best_partition = community_louvain.best_partition(G)
print(best_partition)
communities = {node: (1 if comm == 0 else 2) for node, comm in best_partition.items()}
# communities = best_partition

# Step 3: Highlight important nodes (e.g., by degree centrality)
degree_centrality = nx.degree_centrality(G)
important_nodes = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:2]

# Step 4: Visualize using Pyvis with enhanced layout and node labels
net = Network(notebook=True, height="800px", width="100%", bgcolor="#222222", font_color="white", cdn_resources="in_line")
for node in G.nodes():
    color = "red" if node in important_nodes else f"#{communities[node] * 50 + 150:02x}ff{100:02x}"
    size = 25 if node in important_nodes else 10
    net.add_node(node, label=node, color=color, size=size)

for edge in G.edges(data=True):
    net.add_edge(edge[0], edge[1], title=edge[2]['relation'])

net.show("knowledge_graph.html")

# # Step 5: Matplotlib visualization with smaller font and focus on important nodes
def get_node_color(node):
    return "red" if node in important_nodes else f"#{communities[node] * 50 + 150:02x}ff{100:02x}"
colors = [get_node_color(node) for node in G.nodes()]

pos = nx.spring_layout(G)

plt.figure(figsize=(15, 10))

edge_labels = nx.get_edge_attributes(G, 'relation')  # Extract relations
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)


nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=[500 if node in important_nodes else 100 for node in G.nodes()])
nx.draw_networkx_edges(G, pos, alpha=0.3)
nx.draw_networkx_labels(G, pos, font_size=8, font_color='black')
plt.title("Knowledge Graph with Important Nodes Highlighted")
plt.show()