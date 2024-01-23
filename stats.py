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
    
    def average_degree(self):
        """
        average number of not None keys for each entry of the json files
        """
        self.degrees = []

        for file in self.paths:
            dict = json.load(open(file))

            for x in dict['planet_osm_point']:
                sub_dict = {k:x[k] for k in list(x.keys())[1:-1]}
                res = self._count_not_none(sub_dict)
                self.degrees.append(res)

        return sum(self.degrees)/len(self.degrees)
    
    def common_null_keys(self):
        """
        returns keys that are set to None for all the entries of the json files
        """
        keys = set()

        for file in self.paths:
            dict = json.load(open(file))

            null_count_per_key = {key: 0 for key in list(dict['planet_osm_point'][0].keys())[1:-1]}

            for x in dict['planet_osm_point']:
                for key in list(x.keys())[1:-1]:
                    if x[key] == None:
                        null_count_per_key[key] += 1

            null_keys = []

            for x in null_count_per_key.keys():
                if null_count_per_key[x] == len(dict['planet_osm_point']):
                    null_keys.append(x)

            keys = keys.union(null_keys)
            print(f'{file} : {len(null_keys)}/{len(null_count_per_key.keys())}')

        return keys