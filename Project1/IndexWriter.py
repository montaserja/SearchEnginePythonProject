import re
import pickle
import os


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
        # print(text[0][6:])
        self.file.close()
        dict={}
        for i in range(len(product)):
            dict[i+1]={"product": product[i][11:],"helpfulness":helpfulness[i][13:],"score": score[i][7:],"text":text[i][6:].lower()}
            dict[i+1]["text"]=re.sub("[^a-zA-Z ]+", "", dict[i+1]["text"])
            print(dict[i+1]["text"])
        if(not os.path.isdir(dir)):
            try:
                os.makedirs(dir)
            except OSError:
                print("Creation of the directory %s failed" % dir)

        if read:
            self.fileCreated = open(dir + "/Index.pkl", "wb")
        pickle.dump(dict, self.fileCreated)
        self.fileCreated.close()

    def removeIndex(self, dir):
        """Delete all index files by removing the given
        directory"""
        try:
            os.rmdir(dir)
        except OSError:
            print("Deletion of the directory %s failed" % dir)


dir = "../../Desktop/projectSheltot"
SlowIndexWriter.slowWrite(SlowIndexWriter, dir + "/100.txt", dir)
