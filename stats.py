import json
import os
from math import radians, sin, cos, sqrt, atan2
from itertools import combinations
import random
import numpy as np

class Stats:
    def __init__(self, N: int, folder=os.getcwd()):
        self.paths = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith(".json")]
        self.N = N
    
    def _count_not_none(self, input_dictionary: dict):
        count = 0
        for key in input_dictionary.keys():
            if input_dictionary[key] != None:
                count += 1
        return count
    
    def _extract_x_and_y_for_item(self, input: dict):
        filtered_dict = {key: value for key, value in input.items() if key not in ('x', 'y')}

        return ((input['x'], input['y']), filtered_dict)
    
    def _haversine_distance(self, coord1, coord2):
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
        indexes = range(len(points))

        idx_to_xy = {idx:xy for idx,xy in zip(indexes, points)}
        xy_to_idx = {xy:idx for xy,idx in zip(points, indexes)}

        return idx_to_xy, xy_to_idx
    
    def unique_key_value_pairs(self) -> set:
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
        formatted_edges = []

        for edge in edges:
            node = xy_to_idx[edge[0]]
            abstract_nodes = edge[1]

            for abstract_node in abstract_nodes:
                formatted_edges.append((abstract_node, node))

        return formatted_edges

    def distance_edges(self, nodes: list, idx_to_xy: dict, N:int, treshold=1) -> list:
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
    
    def get_features_from_points(self, points, edges) -> set:
        features = set()
        for edge in edges:
            for point in points:
                if edge[1] == point:
                    features.add(edge[0])
        return features
    
    def draft_features(self, nodes: list, N: int, distance_edges: list, edges: list) -> set:
        center_point = random.choice(nodes)
        neighbours = set()
        for edge in distance_edges:
            if edge[0] == center_point:
                neighbours.add(edge[1])
            elif edge[1] == center_point:
                neighbours.add(edge[0])

        chosen_points = random.sample(list(neighbours), N)
        
        return self.get_features_from_points(chosen_points, edges)

        