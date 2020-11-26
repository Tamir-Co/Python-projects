from functools import total_ordering
import os
import math


class HuffmanTree:
    def __init__(self, data, left, right):
        self.data = data
        self.left = left
        self.right = right


class HuffmanCoding:
    def __init__(self, input_file_path):
        """ init method for class HuffmanCoding.
        input_file_path is a string containing the path to a file which needs to be compressed
        """
        self.compressed_file_path = None
        self.coding_dictionary = dict()

        self.sorted_chars_List = None
        self.huffmanTree = None
        self.frequency_Dict = None
        self.missing_bits = None
        self.txt_in_bytes = None

        self.file_name, self.file_extension = os.path.splitext(os.path.basename(input_file_path))

        with open(input_file_path, 'r' + self.file_extension[1]) as file:
            self.original_text = file.read()
            directory_name = os.path.dirname(input_file_path)
            self.compressed_file_path = os.path.join(directory_name, "compressed_file_" + self.file_name + ".bin")
        self.compress_file()

    def compress_file(self):
        frequency_Dict = dict()
        for char in self.original_text:
            if frequency_Dict.get(char) is None:
                frequency_Dict[char] = 1
            else:
                frequency_Dict[char] += 1
        self.frequency_Dict = frequency_Dict
        self.sorted_chars_List = sorted(frequency_Dict, key=frequency_Dict.__getitem__)

        self.build_tree()
        self.create_coding_dict(self.huffmanTree, '')
        self.change_txt_to_bytes()
        with open(self.compressed_file_path, 'wb') as file:
            file.write(self.txt_in_bytes)

    def build_tree(self):
        huffmanTree = HuffmanTree(self.frequency_Dict[self.sorted_chars_List[0]] +
                                  self.frequency_Dict[self.sorted_chars_List[1]],  # data
                                  self.sorted_chars_List[1],  # left
                                  self.sorted_chars_List[0])  # right
        trees_list = [huffmanTree]
        treelst_size, j = 1, 0
        freqlst_size = len(self.sorted_chars_List)
        i = 2
        while i < freqlst_size:
            next_char = self.sorted_chars_List[i]
            next_freq = self.frequency_Dict[next_char]
            if trees_list[j].data <= next_freq:
                if treelst_size - j > 1:
                    if trees_list[j + 1].data <= next_freq:  # connect 2 trees
                        trees_list.append(HuffmanTree(trees_list[j].data + trees_list[j + 1].data,  # data
                                                      trees_list[j + 1],  # left
                                                      trees_list[j]))  # right
                        treelst_size += 1
                        trees_list[j] = trees_list[j + 1] = None
                        j += 2
                    else:  # connect tree and char
                        trees_list.append(HuffmanTree(next_freq + trees_list[j].data,  # data
                                                      next_char,  # left
                                                      trees_list[j]))  # right
                        treelst_size += 1
                        trees_list[j] = None
                        j += 1
                        i += 1
                else:  # connect tree and char
                    trees_list.append(HuffmanTree(next_freq + trees_list[j].data,  # data
                                                  next_char,  # left
                                                  trees_list[j]))  # right
                    treelst_size += 1
                    trees_list[j] = None
                    j += 1
                    i += 1
            else:  # when trees_list[j].data > next_freq
                if i + 1 < freqlst_size:
                    next_next_char = self.sorted_chars_List[i + 1]
                    next_next_freq = self.frequency_Dict[next_next_char]
                    if trees_list[j].data <= next_next_freq:  # connect tree and char
                        trees_list.append(HuffmanTree(next_freq + trees_list[j].data,  # data
                                                      next_char,  # left
                                                      trees_list[j]))  # right
                        treelst_size += 1
                        trees_list[j] = None
                        j += 1
                        i += 1
                    else:  # connect 2 chars
                        trees_list.append(HuffmanTree(next_freq + next_next_freq,  # data
                                                      next_next_char,  # left
                                                      next_char))  # right
                        treelst_size += 1
                        i += 2
                else:  # connect tree and the last char
                    trees_list.append(HuffmanTree(next_freq + trees_list[j].data,  # data
                                                  next_char,  # left
                                                  trees_list[j]))  # right
                    treelst_size += 1
                    trees_list[j] = None
                    j += 1
                    i += 1
        while treelst_size - j > 1:  # connect 2 trees until they over
            trees_list.append(HuffmanTree(trees_list[j].data + trees_list[j + 1].data,  # data
                                          trees_list[j + 1],  # left
                                          trees_list[j]))  # right
            treelst_size += 1
            trees_list[j] = trees_list[j + 1] = None
            j += 2

        self.huffmanTree = trees_list[j]

    def create_coding_dict(self, tree, code):
        if isinstance(tree, (str, int)):
            self.coding_dictionary[tree] = code
        else:
            self.create_coding_dict(tree.left, code + '0')
            self.create_coding_dict(tree.right, code + '1')

    def change_txt_to_bytes(self):
        str_01 = ""
        txt_in_bytes = bytearray()
        len_st = 0
        for char in self.original_text:
            coding = self.coding_dictionary[char]  # str of "0101..."
            str_01 += coding
            len_st += coding.__len__()
            while len_st > 8:
                txt_in_bytes.append(int(str_01[0:8], 2))
                len_st -= 8
                str_01 = str_01[8::]

        self.missing_bits = 8 - len_st
        str_01 += '0' * self.missing_bits
        txt_in_bytes.append(int(str_01, 2))
        txt_in_bytes.insert(0, self.missing_bits)
        self.txt_in_bytes = txt_in_bytes

    def decompress_file(self, input_file_path):
        """ This method decompresses a previously compressed file.
        Input: input_file_path - path to compressed file.
        Output path to decompressed file (string).
        """
        directory_name = os.path.dirname(input_file_path)
        decompressed_path = os.path.join(directory_name, "decompressed_file_" + self.file_name + self.file_extension)

        if self.file_extension == ".bin":
            with open(input_file_path, 'rb') as compressed_file, \
                    open(decompressed_path, 'wb') as decompressed_file:
                compressed_bytes = compressed_file.read()
                missing_bits = compressed_bytes[0]
                bytes_size = compressed_bytes.__len__()
                i = 1
                path = self.huffmanTree

                while i + 2 <= bytes_size:
                    path_bits = format(compressed_bytes[i], "08b")
                    if i + 2 == bytes_size:
                        path_bits += format(compressed_bytes[i+1], "08b")[0:-missing_bits]
                    for bit in path_bits:
                        if bit == '0':
                            path = path.left
                        else:
                            path = path.right
                        if isinstance(path, int):  # an int is found
                            char = bytes([path])
                            path = self.huffmanTree
                            decompressed_file.write(char)
                    i += 1
        else:  # ".txt"
            with open(input_file_path, 'rb') as compressed_file, \
                    open(decompressed_path, 'wt', newline="\n") as decompressed_file:
                compressed_bytes = compressed_file.read()
                missing_bits = compressed_bytes[0]
                bytes_size = compressed_bytes.__len__()
                i = 1
                path = self.huffmanTree

                while i + 2 <= bytes_size:
                    path_bits = format(compressed_bytes[i], "08b")
                    if i + 2 == bytes_size:
                        path_bits += format(compressed_bytes[i+1], "08b")[0:-missing_bits]
                    for bit in path_bits:
                        if bit == '0':
                            path = path.left
                        else:
                            path = path.right
                        if isinstance(path, str):  # a char is found
                            char = path
                            path = self.huffmanTree
                            decompressed_file.write(char)
                    i += 1
        return decompressed_path

    def calculate_entropy(self):
        """ This method calculates the entropy associated with the distribution
         of symbols in a previously compressed file.
        Input: None.
        Output: entropy (float).
        """
        sum_of_freqs = self.huffmanTree.data
        entropy = 0
        for freq in self.frequency_Dict:
            p = self.frequency_Dict[freq] / sum_of_freqs
            entropy += p * math.log2(p)
        return -entropy


if __name__ == '__main__':
    pass
