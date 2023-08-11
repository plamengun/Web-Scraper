import json


class Context_Manager():
    def __init__(self, path, data) -> None:
        self.path = path
        self.data = data
        
    def __enter__(self):
        self.file_obj = open(self.path, mode="w")
        return self.file_obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file_obj:
            self.file_obj.close()