from __future__ import division
import re
import os
from struct import pack
from struct import unpack

def decode(bytestream):
    """Variable byte code decode.
    Usage:
      import vbcode
      vbcode.decode(bytestream)
        -> [32, 64, 128]
    """
    n = 0
    numbers = []
    bytestream = unpack('%dB' % len(bytestream), bytestream)
    for byte in bytestream:
        if byte < 128:
            n = 128 * n + byte
        else:
            n = 128 * n + (byte - 128)
            numbers.append(n)
            n = 0
    return numbers

def encode_number(number):
    """Variable byte code encode number.
        Usage:
          import vbcode
          vbcode.encode_number(128)
        """
    bytes_list = []
    while True:
        bytes_list.insert(0, number % 128)
        if number < 128:
            break
        number = number // 128
    bytes_list[-1] += 128
    return pack('%dB' % len(bytes_list), *bytes_list)


def encode(numbers):
    """Variable byte code encode numbers.
    Usage:
      import vbcode
      vbcode.encode([32, 64, 128])
    """
    bytes_list = []
    for number in numbers:
        bytes_list.append(encode_number(number))
    return b"".join(bytes_list)

class SlowIndexWriter:



    def slowWrite(self, inputFile, dir):
        """Given product review data, creates an on
        disk index
        inputFile is the path to the file containing
        the review data
        dir is the directory in which all index files
        will be created
        if the directory does not exist, it should be
        created"""
        reviewsize=[]
        wordsinFile = 0
        read = False
        try:  # opens the file to read
            self.file = open(inputFile, 'r')
            read = True
        except OSError as e:
            print(e)

        my_data = self.file.read()
        product = re.findall(r"productId.+", my_data)
        helpfulness =re.findall(r"helpfulness.+",my_data)
        score=re.findall(r"score.+",my_data)
        text=re.findall(r"text:.+",my_data)
        self.file.close()
        dict={}
        if(not os.path.isdir(dir)):
            try:
                os.makedirs(dir)
            except OSError:
                print("Creation of the directory %s failed" % dir)

        if read:
            if(os.path.isfile(dir+"\words.txt")):
                os.remove(dir+"\words.txt")
            with open(dir+"\index.txt", "wb") as self.binary_file:
                # Write text or bytes to the file
                leng=0;
                for i in range(len(product)):

                    stringToWrite=product[i][11:]
                    for c in stringToWrite:
                        self.binary_file.write(encode_number(ord(c)))
                    self.binary_file.write(encode_number(int(float(score[i][7:]))))
                    stringToWrite = helpfulness[i][13:]
                    for c in stringToWrite:
                        self.binary_file.write(encode_number(ord(c)))
                    text[i] = re.sub("[^a-zA-Z0-9]+", " ", text[i])
                    my_text = text[i][5:].lower()
                    txt_length=len(my_text)

                    # self.binary_file.write(encode_number(txt_length))
                    arr=my_text.split(" ")
                    reviewsize.append(len(arr)-1)
                    wordsfileOp="wb"
                    if os.path.isfile(dir + "\words.txt"):
                        wordsfileOp="ab"#if you want to apent to file just write "ab"
                    #word arr[freq] arr[index] arr[]
                    with open(dir + "\words.txt", wordsfileOp) as words:
                        for idx,word in enumerate(arr):
                            if word in dict.keys():
                                if i in dict[word]["freq"].keys():
                                    dict[word]["freq"][i] += 1
                                    dict[word]["place"][i].append(idx)
                                else:
                                    dict[word]["freq"][i] = 1
                                    dict[word]["place"][i] = [idx]
                                dict[word]["totalFreq"] += 1
                                wordsinFile +=1
                            else:
                                words.write(word.encode('utf8'))
                                words.write("\n".encode('utf8'))
                                dict[word] = {"indexInWordsFile":0,"totalFreq":1,"freq":{},"place":{}}
                                dict[word]["indexInWordsFile"]=leng
                                leng += len(word)
                                wordsinFile += 1
                                dict[word]["freq"][i]=1
                                dict[word]["place"][i]=[idx]
                    self.binary_file.write("\n".encode('utf8'))
            with open(dir + "\TotalFreq.txt", "wb") as TotalFreq:
                TotalFreq.write(encode_number(wordsinFile))
                TotalFreq.write("\n".encode('utf8'))

                for s,freq in enumerate(reviewsize):
                    TotalFreq.write(str(freq).encode('utf8'))
                    TotalFreq.write("\n".encode('utf8'))

            with open(dir + "\data.txt", "wb") as data:
                for word in dict:
                    data.write(encode(dict[word]["freq"]))
                    data.write("\n".encode('utf8'))
                    data.write(encode(dict[word]["freq"].values()))
                    data.write("\n".encode('utf8'))

    def removeIndex(self, dir):
        """Delete all index files by removing the given
        directory"""
        try:
            os.rmdir(dir)
        except OSError:
            print("Deletion of the directory %s failed" % dir)


dir = "../projectSheltot"
SlowIndexWriter.slowWrite(SlowIndexWriter, dir + "/100.txt", dir)
