from pyspark.sql import SparkSession
from graphframes import GraphFrame

class PageRank:
	def __init__(self, fileName) -> None:
		self.fileName = fileName
		self.sparkSession = SparkSession.builder.appName("PageRank").getOrCreate()
		self.graph = self.__loadGraphFrame__()

	def __loadGraphFrame__(self) -> None:
		with open(self.fileName, 'r') as f:
			lines = f.readlines()
			vertices = []
			edges = []
			for line in lines:
				vertex, pageRank, numNeighbors, *neighbors = line.split()
				vertices.append((vertex, {'pageRank' : float(pageRank), 'numNeighbors' : int(numNeighbors)}))
				for neighbor in neighbors:
					edges.append((vertex, neighbor))

		graph = GraphFrame(self.sparkSession.createDataFrame(vertices, 
						   								  	 ['id', 'pageRank']), 
						   self.sparkSession.createDataFrame(edges, 
						   								  	 ['src', 'dst']))
		
		return graph

	def run(self, dampingFactor : float = 0.85, maxIter : int = 10) -> GraphFrame:
		result = self.graph.pregel \
						   .setMaxIter(maxIter) \
						   .withVertexColumn('pageRank', self.graph.vertices['pageRank']) \
						   .sendMsgToDst(lambda triplet: [(triplet.src["id"], triplet.src["pagerank"] / len(triplet.src["pagerank"]))]) \
						   .aggMsgs(lambda msgs: 1-dampingFactor + dampingFactor * sum(msgs)) \
						   .run()
		
		return result
	
	def viewReults(self) -> None:
		self.graph.vertices.show()
		self.graph.edges.show()

if __name__ == '__main__':
	pagerank = PageRank('../MapReduce/input/input.txt')
	pagerank.run()
	pagerank.viewReults()