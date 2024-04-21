from pyvis.network import Network

def visualizePageRanks():
	net = Network(directed=True)
	graph = {}

	with open('./output/output.txt', 'r') as f:
		lines = f.readlines()
		for line in lines:
			vertex, pageRank, numNeighbors, *neighbors = line.split()
			print(vertex, pageRank, numNeighbors, neighbors)

			if vertex not in graph:
				graph[vertex] = {'index': len(graph), 'neighbors': neighbors}

			net.add_node(vertex, label=graph[vertex]['index'], value=float(pageRank))
			
		for node in graph:
			for neighbor in graph[node]['neighbors']:
				net.add_edge(node, neighbor)

	net.show('visualisation.html')

if __name__ == '__main__':
	visualizePageRanks()
		