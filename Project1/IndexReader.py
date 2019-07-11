"""
    Montaser Jafrah 316367838
    Ibrahim Idkedek 205860968
"""
from __future__ import division
import os




class IndexReader:

    def binarySearch(self,arr, l, r, x):

        # Check base case
        if r >= l:

            mid = int(l + (r - l) / 2)

            # If element is present at the middle itself
            if mid == x:
                return arr[mid-1]

                # If element is smaller than mid, then it
            # can only be present in left subarray
            elif mid > x:
                return self.binarySearch(arr, l, mid - 1, x)

                # Else the element can only be present
            # in right subarray
            else:
                return self.binarySearch(arr, mid + 1, r, x)

        else:
            # Element is not present in the array
            return -1





    def readIndexFile(self,type,reviewId,nullreturn):
        """this function reads the index.txt file and returns thae reviewid (type) data """
        if reviewId<=0:
            return nullreturn
        datatoreturn=nullreturn
        if self.found:
            try:  # opens the file to read
                file = open(self.dir + "\\index.txt", 'r')
            except OSError as e:
                print(e)
            size=0
            while True:
                block=file.readlines(536870912*2)#536870912*2
                length=len(block)
                size+=length
                if not block:
                    break
                if reviewId < size:
                    numTorm=size-length
                    half =int( length / 2)
                    if type=="id":
                        datatoreturn= self.binarySearch(block,0,length,reviewId-numTorm)[:self.productIdLen]
                    elif type=="score":
                        datatoreturn = int(self.binarySearch(block, 0, length, reviewId - numTorm)[-2])
                    elif type == "numerator":
                        line=self.binarySearch(block, 0, length, reviewId - numTorm)
                        line=self.binarySearch(block,0,length,reviewId-numTorm)[self.productIdLen:-2]
                        datatoreturn =int(line[:line.find("/")])
                    elif type == "denominator":
                        line = self.binarySearch(block, 0, length, reviewId - numTorm)
                        line = self.binarySearch(block, 0, length, reviewId - numTorm)[self.productIdLen:-2]
                        datatoreturn= int(line[line.find("/")+1:])

                    file.close()
                    del block
                    break

        file.close()
        return datatoreturn

    def readWordsFile(self,token):
        """this function reads the words.txt file and call the readDataFile with the index of the token"""
        if self.found:
            try:  # opens the file to read
                file = open(self.dir + "\\words.txt", 'r')
            except OSError as e:
                print(e)
            for i,word in enumerate(file):
                if word[:-1]==token:
                    file.close()
                    return i
            file.close()
            return -1

    def readDataFile(self,i):
        arr=[]
        try:  # opens the file to read
            file = open(self.dir + "\\data.txt", 'r')
            size = 0
            while True:
                block = file.readlines(536870912*2)  # 536870912*2
                length = len(block)
                size += length
                if not block:
                    break
                if i <= size:
                    numTorm = size - length
                    temp=self.binarySearch(block, 0, length, i - numTorm)
                    del block
                    return temp
        except OSError as e:
            print(e)


    def __init__(self, dir):
        """Creates an IndexReader which will read from
        the given directory"""
        self.found = False
        self.dir=dir+"/files"
        if os.path.isdir(dir):
            if os.path.isfile(dir+"/files/Index.txt"):
                    self.found=True
                    self.productIdLen=10
            else:
                print("file not found")
        else:
            print("dir Not Found")



    def getProductId(self, reviewId):
        """Returns the product identifier for the given
        review
        Returns null if there is no review with the
        given identifier"""
        return self.readIndexFile("id",reviewId,None)


    def getReviewScore(self, reviewId):
        """Returns the score for a given review
        Returns -1 if there is no review with the given
        identifier"""
        return self.readIndexFile("score",reviewId,-1)

    def getReviewHelpfulnessNumerator(self, reviewId):
        """Returns the numerator for the helpfulness of
        a given review
        Returns -1 if there is no review with the given
        identifier"""
        return self.readIndexFile("numerator",reviewId,-1)

    def getReviewHelpfulnessDenominator(self, reviewId):
        """Returns the denominator for the helpfulness
        of a given review
        Returns -1 if there is no review with the given
        identifier"""
        return self.readIndexFile("denominator",reviewId,-1)

    def getReviewLength(self, reviewId):
        """Returns the number of tokens in a given
        review
        Returns -1 if there is no review with the given
        identifier"""
        if reviewId<=0:
            return -1
        try:  # opens the file to read
            file = open(self.dir + "\\TotalFreq.txt", 'r')
        except OSError as e:
            print(e)
        size = 0
        while True:
            block = file.readlines(536870912 * 2)  # 536870912*2
            length = len(block)
            size += length
            if not block:
                break
            if reviewId < size:
                numTorm = size - length
                file.close()
                try:
                    return int(self.binarySearch(block, 0, length, reviewId - numTorm)[:-1])
                except:
                    return -1

        return -1

    def getTokenFrequency(self, token):
        """Return the number of reviews containing a
        given token (i.e., word)
        Returns 0 if there are no reviews containing
        this token"""
        wordIndex=self.readWordsFile(token)
        if wordIndex==-1:
            return 0
        arr=self.readDataFile(wordIndex+1)[:-1].split(',')
        arr=list(dict.fromkeys(arr))
        return len(arr)-1

    def getTokenCollectionFrequency(self, token):
        """Return the number of times that a given
        token (i.e., word) appears in
        the reviews indexed
        Returns 0 if there are no reviews containing
        this token"""
        wordIndex = self.readWordsFile(token)
        if wordIndex == -1:
            return 0
        arr = self.readDataFile(wordIndex + 1)[:-1].split(',')
        return len(arr)-1

    def get_reviews_with_token_text(self,id,freq):
        return "id-"+str(id)+", freq-"+str(freq)

    def getReviewsWithToken(self, token):
        """Returns a series of integers of the form id1, freq-1, id-2, freq-2, ... such
        that id-n is the n-th review containing the
        given token and freq-n is the
        number of times that the token appears in
        review id-n
        Note that the integers should be sorted by id
        Returns an empty Tuple if there are no reviews
        containing this token"""
        wordIndex = self.readWordsFile(token)
        if wordIndex == -1:
            return ()
        arr = self.readDataFile(wordIndex + 1)[:-1].split(',')

        arr=arr[1:]
        prev="0"
        count=0
        str = []
        for i,item in enumerate(arr):
            if i==0:
                prev=item
            else:
                if item==prev:
                    count+=1
                else:
                    str.append((int(prev),count+1))
                    count=0
                    prev=item
                if i==len(arr)-1:
                    str.append((int(item), count+1))
        return tuple(str)


    def getNumberOfReviews(self):
        """Return the number of product reviews
        available in the system"""
        try:  # opens the file to read
            file = open(self.dir + "\\TotalFreq.txt", 'r')
        except OSError as e:
            print(e)
        size=0
        while True:
            block = file.readlines(536870912 * 2)  # 536870912*2
            length = len(block)
            size += length
            if not block:
                break
        file.close()
        return size

    def getTokenSizeOfReviews(self):
        """Return the number of tokens in the system
        (Tokens should be counted as many times as they
        appear)"""
        try:  # opens the file to read
            file = open(self.dir + "\\TotalFreq.txt", 'r')
        except OSError as e:
            print(e)
        size = 0
        while True:
            block = file.readlines(536870912 * 2)  # 536870912*2
            for line in block:
                size+=int(line[:-1])
            if not block:
                break

        return size

    def getProductReviews(self, productId):
        """Return the ids of the reviews for a given
        product identifier
        Note that the integers returned should be
        sorted by id
        Returns an empty Tuple if there are no reviews
        for this product"""
        ids = []
        if self.found:
            try:  # opens the file to read
                file = open(self.dir + "\\index.txt", 'r')
                for i,line in enumerate(file):
                    if line[:self.productIdLen]==productId:
                        ids.append(i+1)
                file.close()
            except OSError as e:
                print(e)
        return tuple(ids)
"""
import datetime
dir = "../projectSheltot"
reader=IndexReader(dir)
x = datetime.datetime.now()
print(x)
print(reader.getReviewsWithToken("is"))
x2=datetime.datetime.now()
print(x2-x)
"""