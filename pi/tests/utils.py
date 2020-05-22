import ast
# from sys import argv
#script, data = argv

def convert_byte_to_dict(byte_str):
    dict_str = byte_str.decode("UTF-8")
    data = ast.literal_eval(dict_str)
    # print(data)
    return data