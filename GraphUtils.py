import json
import os
from math import radians, sin, cos, sqrt, atan2
import random
import numpy as np

class GraphUtils:
    """
    Class that contains utility functions for graphs, such as nodes and edges creation.
    It uses the given folder path to search for json files in which to look.
    Only the N firsts entries of the json files are considered. For simplifying neighbours computation,
    N has to be a perfect square. 
    """
    def __init__(self, N: int, folder=os.getcwd()):
        self.paths = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith(".json")]
        self.N = N

        sq_root = int(sqrt(self.N))
        if sq_root * sq_root != N:
            raise ValueError("N has to be a perfect square.")
    
    def _count_not_none(self, input_dictionary: dict):
        count = 0
        for key in input_dictionary.keys():
            if input_dictionary[key] != None:
                count += 1
        return count
    
    def _extract_x_and_y_for_item(self, input: dict):
        """
        Extracts X and Y column from a given input of a json file.
        """
        filtered_dict = {key: value for key, value in input.items() if key not in ('x', 'y')}

        return ((input['x'], input['y']), filtered_dict)
    
    def _haversine_distance(self, coord1, coord2):
        """
        Computes distance between two points using Haversine formula.
        """
        R = 6371.0

        lon1, lat1 = coord1
        lon2, lat2 = coord2

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        return distance

    def average_degree(self) -> float:
        """
        average number of not None keys for each entry of the json files
        """
        self.degrees = []

        for file in self.paths:
            data = json.load(open(file))

            for x in data:
                _, sub_dict = self._extract_x_and_y_for_item(x)
                res = self._count_not_none(sub_dict)
                self.degrees.append(res)

        return sum(self.degrees)/len(self.degrees)
    
    def common_null_keys(self) -> set:
        """
        returns keys that are set to None for all the entries of the json files
        """
        keys = set()

        for file in self.paths:
            data = json.load(open(file))

            _, sub_dict = self._extract_x_and_y_for_item(data[0])
            null_count_per_key = {key: 0 for key in sub_dict}

            for x in data:
                _, sub_dict = self._extract_x_and_y_for_item(x)
                for key in sub_dict:
                    if x[key] == None:
                        null_count_per_key[key] += 1

            null_keys = []

            for x in null_count_per_key.keys():
                if null_count_per_key[x] == len(data):
                    null_keys.append(x)

            keys = keys.union(null_keys)
            print(f'{file} : {len(null_keys)}/{len(null_count_per_key.keys())}')

        return keys
    
    def mapping_dictionaries(self, points: list) -> (dict, dict):
        """
        Returns two mapping dictionnaries for the given points list.
        xy_to_idx dictionary maps points (as (latitude,longitude) tuple) to indexes.
        idx_to_xy maps indexes to (latitude,longitude) tuple.
        """
        indexes = range(len(points))

        idx_to_xy = {idx:xy for idx,xy in zip(indexes, points)}
        xy_to_idx = {xy:idx for xy,idx in zip(points, indexes)}

        return idx_to_xy, xy_to_idx
    
    def unique_key_value_pairs(self) -> set:
        """
        Returns all unique key,value pairs in all the dictionaries contained in the json files, except the coordinates.
        These values are used as abstract nodes in graphs.
        """
        self.unique_key_value = set()
        treated_nodes: int = 0

        for file in self.paths:
            data = json.load(open(file))

            for x in data:
                treated_nodes += 1
                _, sub_dict = self._extract_x_and_y_for_item(x)

                for key in sub_dict.keys():
                    if sub_dict[key] != None:
                        name = f'{key}/{sub_dict[key]}'
                        self.unique_key_value.add(name)
                if treated_nodes >= self.N:
                    return self.unique_key_value
                

        return self.unique_key_value
    
    def nodes(self) -> set:
        """
        Returns all nodes found in the json files, as (latitude,longitude) tuples
        """
        nodes = set()

        for file in self.paths:
            data = json.load(open(file))

            for x in data:
                coords, _ = self._extract_x_and_y_for_item(x)
                nodes.add(coords)
                if len(nodes) >= self.N:
                    return nodes

        return nodes

    def edges(self) -> list:
        """
        Computes the relations between geographic nodes and its features as edges.
        Returns a list of tuples containing a geographic node and the list of its features (geo_node,[features..])
        """
        edges = []

        for file in self.paths:
            data = json.load(open(file))

            for x in data:
                coords, sub_dict = self._extract_x_and_y_for_item(x)
                neighbours = []
                for key in sub_dict.keys():
                    if sub_dict[key] != None:
                        name = f'{key}/{sub_dict[key]}'
                        neighbours.append(name)

                edges.append(((coords), neighbours))
                if len(edges) >= self.N:
                    return edges
            
        return edges
    
    def edges_formatting(self, edges: list, xy_to_idx: dict) -> list:
        """
        Formats the edges (returned from edges) function in order to fit with networkx specs 
        """
        formatted_edges = []

        for edge in edges:
            node = xy_to_idx[edge[0]]
            abstract_nodes = edge[1]

            for abstract_node in abstract_nodes:
                formatted_edges.append((abstract_node, node))

        return formatted_edges

    def distance_edges(self, nodes: list, idx_to_xy: dict, N:int, treshold=1) -> list:
        """
        Computes edges between close points. Treshold is used to adjust the limit to cosider if points are closed enough
        to be linked.
        """
        size = int(np.sqrt(len(nodes)))
        if size * size != len(nodes):
            raise ValueError("Input list length is not a perfect square.")

        matrix = np.array(nodes).reshape(size, size)

        edges = []

        for i in range(size):
            for j in range(size):
                # Compute the coordinates of the N * N square centered on (i, j)
                start_row = max(0, i - N // 2)
                end_row = min(size, i + N // 2 + 1)
                start_col = max(0, j - N // 2)
                end_col = min(size, j + N // 2 + 1)

                neighbours = list(matrix[start_row:end_row, start_col:end_col].flatten())
                neighbours.remove(matrix[i,j])

                center_coords = idx_to_xy[matrix[i,j]]

                for neighbour in neighbours:
                    neighbour_coords = idx_to_xy[neighbour]
                    if self._haversine_distance(center_coords, neighbour_coords) <= treshold:
                        edges.append((matrix[i,j],neighbour))

        return edges
    
    def get_features_from_points(self, nodes, edges) -> set:
        """
        Returns the corresponding features for a list of given nodes
        """
        features = set()
        for edge in edges:
            for point in nodes:
                if edge[1] == point:
                    features.add(edge[0])
        return features
    
    def draft_features(self, nodes: list, N: int, distance_edges: list, edges: list) -> set:
        """
        Returns a set of at least two features to test our graph algorithm.
        """
        def _draft_features(self, nodes: list, N: int, distance_edges: list, edges: list):
            center_point = random.choice(nodes)
            neighbours = set()
            for edge in distance_edges:
                if edge[0] == center_point:
                    neighbours.add(edge[1])
                elif edge[1] == center_point:
                    neighbours.add(edge[0])

            if len(neighbours) < N:
                chosen_points = neighbours
            else:
                chosen_points = random.sample(list(neighbours), N)

            features = self.get_features_from_points(chosen_points, edges)

            return features
        
        features = _draft_features(self, nodes, N, distance_edges, edges)
        while len(features) < 2:
            features = _draft_features(self, nodes, N, distance_edges, edges)
        return features