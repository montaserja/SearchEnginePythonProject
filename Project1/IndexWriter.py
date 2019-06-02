import re
import pickle
import os
import binascii


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
        #print(helpfulness)
        # print(product)
        # print(score)
        # print(text)
        # print(product[0][11:])
        #print(helpfulness[0][13:])
        # print(score[0][7:])
        # print(text[0][5:])
        self.file.close()
        dict={}
        """
        for i in range(len(product)):
            dict[i+1]={"product": product[i][11:],"helpfulness":helpfulness[i][13:],"score": score[i][7:],"text":text[i][5:].lower()}
            dict[i+1]["text"]=re.sub("[^a-zA-Z ]+", "", dict[i+1]["text"])
            print(dict[i+1]["text"])
            """
        if(not os.path.isdir(dir)):
            try:
                os.makedirs(dir)
            except OSError:
                print("Creation of the directory %s failed" % dir)

        if read:
            with open(dir+"\index.txt", "wb") as self.binary_file:
                # Write text or bytes to the file
                leng=0;
                for i in range(len(product)):
                    #self.binary_file.write(i.to_bytes(4, byteorder='big'))
                    self.binary_file.write(product[i][11:].encode('utf8'))
                    self.binary_file.write(helpfulness[i][13:].encode('utf8'))
                    self.binary_file.write(int(float(score[i][7:])).to_bytes(1, byteorder='big'))
                    #print(bin(int(binascii.hexlify('hello'), 16)))
                    text[i] = re.sub("[^a-zA-Z0-9]+", " ", text[i])
                    my_text = text[i][5:].lower()
                    arr=my_text.split(" ")
                    #word arr[freq] arr[index] arr[]

                    for word in arr:
                        if word in dict.keys():
                            if i in dict[word]["freq"].keys():
                                dict[word]["freq"][i] += 1
                            else:
                                dict[word]["freq"][i] = 1
                            dict[word]["totalFreq"] += 1
                        else:
                            dict[word] = {"indexInWordsFile":0,"totalFreq":1,"freq":{}}
                            dict[word]["indexInWordsFile"]=leng
                            leng+=len(word)
                            dict[word]["freq"][i]=1


                    self.binary_file.write("\n".encode('utf8'))

                    #self.binary_file.write((text[i][6:].lower()).encode('utf8'))
                    #self.binary_file.write("\n".encode('utf8'))


                #num_bytes_written = self.binary_file.write(b'\xDE\xAD\xBE\xEF')
                #print("Wrote %d bytes." % num_bytes_written)

    def removeIndex(self, dir):
        """Delete all index files by removing the given
        directory"""
        try:
            os.rmdir(dir)
        except OSError:
            print("Deletion of the directory %s failed" % dir)


dir = "../../Desktop/projectSheltot"
SlowIndexWriter.slowWrite(SlowIndexWriter, dir + "/100.txt", dir)
