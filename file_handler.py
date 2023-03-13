"""
This class reads vocabulary words from given file

This file has to have a specific structure to be parsable 
successfully


"""

class FileHandler:
    file_name: str
    file_path: str
    voc_list: tuple = ()

    def __init__(self, file_name: str, file_path: str = ".") -> None:
        self.file_name = file_name
        self.file_path = file_path
        self.open_file(file_path + "/" + file_name)



    def open_file(self, path_to_file):
        try:
            with open(path_to_file, encoding='utf-8') as f:
                file_content = f.readlines()
            self.parse_file(file_content)
        except Exception as e:
            print(f"Failed to read due {e}")


    def parse_file(self, file_content):
        lines = (line.rstrip() for line in file_content)
        lines = list(lines)
        res_dict = map(lambda i: (lines[i], lines[i+1], lines[i+2]), range(len(lines)-2)[::3])
        self.voc_list = tuple(res_dict)
        print( self.voc_list)
    
    def get_voc_list(self):
        return self.voc_list
    

    def write_voc(self, voc = tuple):
        try:
            with open('voc2.txt', 'w') as f:
                [f.writelines(i+"\n") for item in self.voc_list for i in item]
                f.close()
        except Exception as e:
            print(f"Failed to write to file due {e}")

