import re
import os
import datetime
import sys

class IndexWriter:
    def write(self, inputFile, dir):
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
            file = open(inputFile, 'r')
            read = True
        except OSError as e:
            print(e)
        onePruduct = ""
        oneScore = ""
        oneHelp = ""
        oneText = ""
        idx = 1  # the index of the review in my dict
        fileNum = 1
        dirNum = 1
        wordsDict = {}
        dict = {}
        if (not os.path.isdir(dir)):  # creates the dir if not exist
            try:
                os.makedirs(dir)
            except OSError:
                print("Creation of the directory %s failed" % dir)
        try:  # opens the file to read
            textFile = open(dir + "\\texts.txt", 'w')
        except OSError as e:
            print(e)
        try:  # opens the file to read
            indexFile = open(dir + "\index.txt", 'w')
        except OSError as e:
            print(e)
        try:  # opens the file to read
            FreqFile = open(dir + "\TotalFreq.txt", 'w')
        except OSError as e:
            print(e)

        while True:
            block = file.readlines(int(536870912/2))  # 536870912 bytes ----> 0.5 GB
            if not block :
                break
            for i, item in enumerate(block):
                if (item.startswith("product/productId:")):
                    # print(item[19:])
                    onePruduct = item[19:-1]
                elif (item.startswith("review/helpfulness:")):
                    # print(item[20:])
                    oneHelp = item[20:-1]
                elif (item.startswith("review/score: 1.0")):
                    # print(item[14:])
                    oneScore = int(float(item[14:-1]))
                elif (item.startswith("review/text:")):
                    # print(item[13:])
                    oneText = item[13:-1]
                elif (item.startswith("\n")):
                    if (oneScore != "" and oneText != "" and oneHelp != "" and onePruduct != ""):
                        dict[idx] = {"product": onePruduct, "helpfulness": oneHelp, "score": oneScore, "text": oneText}
                        idx += 1
            del block
            for index, item in enumerate(dict):
                indexFile.write(dict[item]["product"])
                indexFile.write(dict[item]["helpfulness"])
                indexFile.write(str(dict[item]["score"]))
                del dict[item]["product"]
                del dict[item]["helpfulness"]
                del dict[item]["score"]
                dict[item]["text"] = re.sub("[^a-zA-Z0-9]+", " ", dict[item]["text"])
                dict[item]["text"]=dict[item]["text"].lower()
                wordsListFromText = re.split(" +", dict[item]["text"])
                FreqFile.write(str(len(wordsListFromText)))
                FreqFile.write("\n")
                textFile.write(dict[item]["text"])
                textFile.write("\n")
                del dict[item]["text"]
                for word in wordsListFromText:
                    wordsDict[word]=""
                del wordsListFromText
                indexFile.write("\n")
            del dict
            dict = {}
        indexFile.close()
        textFile.close()
        words= sorted(wordsDict.keys())
        #del wordsDict #------------>   ibra
        file.close()

        # ibra ----------------------------------------------------------------------------------------------------------
        x = datetime.datetime.now()
        print('the merge start ', x)
        wordsdir=dir+"\wordsdir"
        try:  # opens the file to read
            wordsfile = open(dir + "\\words.txt", 'w')
        except OSError as e:
            print(e)

        for index,word in enumerate(words):
            if word!='':
                wordsDict[word] = index
                wordsfile.write(word + '\n')


        if (not os.path.isdir(wordsdir)):  # creates the dir if not exist
            try:
                os.makedirs(wordsdir)
            except OSError:
                print("Creation of the directory %s failed" % wordsdir)

        try:  # opens the file to read
            textFile = open(dir + "\\texts.txt", 'r')
        except OSError as e:
            print(e)
        counter = 0
        revcounter = 0
        filesname = []
        xDict = {}
        while True:
            block = textFile.readline()  # 536870912 bytes ----> 0.5 GB
            revcounter +=1
            if not block and block != '\n':
                textFile.close()
                break

            wordss=re.split(" +", block[:-1])
            for word in wordss:
                if word not in xDict:
                    xDict[word]=[revcounter]
                else:
                    xDict[word].append(revcounter)

                if sys.getsizeof(xDict) >= int(20971520*2):#(20971520*2)
                    try:  # opens the file to write
                        textFile1 = open(wordsdir + "/file" + str(counter) + ".txt", 'w')
                        counter += 1
                    except OSError as e:
                        print(e)
                    for word1 in sorted(xDict.keys()):
                        for i in xDict[word1]:
                            textFile1.write(str(wordsDict[word1]) + "," + str(i) + '\n')
                    textFile1.close()
                    xDict.clear()

        if len(xDict.keys())>0:
            try:  # opens the file to write
                textFile1 = open(wordsdir + "/file" + str(counter) + ".txt", 'w')
                counter += 1
            except OSError as e:
                print(e)
            for word in sorted(xDict.keys()):
                for i in xDict[word]:
                    textFile1.write(str(wordsDict[word]) + "," + str(i) + '\n')
            xDict.clear()
            del xDict
        textFile1.close()
        textFile.close()
        files = os.listdir('../projectSheltot\\files\\wordsdir')
        count = 0
        while len(files)>1:
            for i in range(0, len(files), 2):
                if i < len(files) - 1:
                    marginFiles('../projectSheltot\\files\\wordsdir\\', files[i], files[i+1], count)
                    count += 1
                    break
            files = os.listdir('../projectSheltot\\files\\wordsdir')


        try:  # opens the file to read
            mergedFil = open('../projectSheltot\\files\\wordsdir\\' + files[0] , 'r')
        except OSError as e:
            print(e)

        try:  # opens the file to read
            data = open('../projectSheltot\\files\\data.txt' , 'w')
        except OSError as e:
            print(e)

        last = 1
        while True:
            block= mergedFil.readlines(int(536870912/2))
            if not block:
                break
            itemList=[]

            for item in block:
                psiq=item.find(',')
                if psiq!=0:
                    if item[:psiq]==str(last):
                        itemList.append(item[psiq+1:-1])
                    else:
                        data.write(str(last))
                        for zobor in itemList:
                            data.write(",")
                            data.write(zobor)
                        data.write("\n")
                        itemList=[]
                        itemList.append(item[psiq + 1:-1])
                        last=item[:psiq]
        if len(itemList)>0:
            data.write(str(last))
            for zobor in itemList:
                data.write(",")
                data.write(zobor)
            data.write("\n")
            itemList = []
        mergedFil.close()

        try:  # opens the file to read
            os.remove('../projectSheltot\\files\\wordsdir\\' + files[0])
            os.rmdir('../projectSheltot\\files\\wordsdir\\')
            del files
        except OSError as e:
            print(e)




def marginFiles(dir, file1,file2, counter):
    try:  # opens the file to read
        file1 = open(dir + file1, 'r')
        file2 = open(dir + file2, 'r')
    except OSError as e:
        print(e)
    try:
        mergedFile = open(dir + "\merginefile" + str(counter) + ".txt", 'w')
    except OSError as e:
        print(e)
    if os.path.exists(str(file1.name)):
        line1 = file1.readline()
    else:
        line1 = None

    if os.path.exists(str(file2.name)):
        line2 = file2.readline()
    else:
        line2 = None
    while True:

        if not line1:
            if not line2:
                mergedFile.close()
                file1.close()
                file2.close()
                os.remove(str(file1.name))
                os.remove(str(file2.name))
                return
            else:
                mergedFile.write(line2)
                line2 = file2.readline()
        elif not line2:
            mergedFile.write(line1)
            line1 = file1.readline()
        elif line1 >= line2:
            mergedFile.write(line2)
            line2 = file2.readline()
        elif line2 > line1:
            mergedFile.write(line1)
            line1 = file1.readline()


def removeIndex(self, dir):
        """Delete all index files by removing the given
        directory"""


dir = "../projectSheltot"
x = datetime.datetime.now()
print(x)
IndexWriter.write(IndexWriter, dir + "/Books1000000.txt", dir+"\\files")
x2=datetime.datetime.now()
print(x2-x)