import json
import os

class DirTree:
    def __init__(self, db_path):
        self.tree = {}
        self.db_path = db_path
        
    def save_tree(self):
        with open("dir_tree.json", "w") as treefile:
            json.dump(self.tree, treefile)

    def make_tree(self)->dict:
        dirs = os.listdir(self.db_path)
        for folder in dirs:
            try:
                files = os.listdir(os.path.join(self.db_path, folder))
            except:
                continue
            self.tree[folder]=files
        self.save_tree()
        return self.tree
    
    def init_tree(self):
        with open('dir_tree.json') as data:
            self.tree = json.load(data)
        return self.tree
    
    def update_tree(self, name, file_name):
        value = self.tree.get(name,[])
        value.append(file_name)
        self.tree[name] = value
        self.save_tree()