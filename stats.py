import json
import os

class Stats:
    def __init__(self, folder=os.getcwd()):
        self.paths = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith(".json")]

    def _common_elements(self, arr1: list, arr2: list, arr3: list):
        set1 = set(arr1)
        set2 = set(arr2)
        set3 = set(arr3)

        common_set = set1.intersection(set2, set3)
        common_list = list(common_set)

        return common_list
    
    def _count_not_none(self, input_dictionary: dict):
        count = 0
        for key in input_dictionary.keys():
            if input_dictionary[key] != None:
                count += 1
        return count
    
    def _extract_x_and_y_for_item(self, input: dict):
        filtered_dict = {key: value for key, value in input.items() if key not in ('x', 'y')}

        return ((input['x'], input['y']), filtered_dict)

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
    
    def _mapping_dictionaries(self, points: list) -> (dict, dict):
        indexes = range(len(points))

        idx_to_xy = {idx:xy for idx,xy in zip(indexes, points)}
        xy_to_idx = {xy:idx for xy,idx in zip(points, indexes)}

        return idx_to_xy, xy_to_idx
    
    def unique_key_value_pairs(self) -> set:
        self.unique_key_value = set()

        for file in self.paths:
            data = json.load(open(file))

            for x in data:
                _, sub_dict = self._extract_x_and_y_for_item(x)

                for key in sub_dict.keys():
                    if sub_dict[key] != None:
                        name = f'{key}/{sub_dict[key]}'
                        self.unique_key_value.add(name)

        return self.unique_key_value
    
    def nodes(self) -> set:
        nodes = set()

        for file in self.paths:
            data = json.load(open(file))

            for x in data:
                coords, _ = self._extract_x_and_y_for_item(x)
                nodes.add(coords)

        return nodes

    def connexions(self) -> list:
        connexions = []

        for file in self.paths:
            data = json.load(open(file))

            for x in data:
                coords, sub_dict = self._extract_x_and_y_for_item(x)
                neighbours = []
                for key in sub_dict.keys():
                    if sub_dict[key] != None:
                        name = f'{key}/{sub_dict[key]}'
                        neighbours.append(name)

                connexions.append(((coords), neighbours))
            
        return connexions
