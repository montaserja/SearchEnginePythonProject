from __future__ import division
import os
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

class IndexReader:

    def readIndexFile(self,type,reviewId,nullreturn):
        """this function reads the index.txt file and returns thae reviewid (type) data """
        datatoreturn=nullreturn
        if self.found:
            with open(self.dir + "\index.txt", "rb") as data:
                for i, line in enumerate(data):
                    if reviewId - 1 == i:
                        id = decode(line)
                        if type=="score":
                            datatoreturn=id[self.productIdLen]
                            break
                        elif type=="id":
                            datatoreturn= ''.join(chr(i) for i in id[:self.productIdLen])
                            break
                        elif type=="numerator":
                            count=0
                            for idx,c in enumerate(id):
                                if c==47:
                                    break
                                count += 1
                            datatoreturn = int(''.join(chr(i) for i in id[self.productIdLen+1:count]))
                            #datatoreturn=int(chr(id[self.productIdLen:length]))
                        elif type=="denominator":
                            count = 0
                            for idx, c in enumerate(id):
                                if c == 47:
                                    break
                                count += 1
                            datatoreturn = int(''.join(chr(i) for i in id[count+1:]))
                    elif type=="ReviewsNum":
                        datatoreturn=i
                    elif reviewId - 1 < i:
                        break
        return datatoreturn

    def readWordsFile(self,token):
        """this function reads the words.txt file and call the readDataFile with the index of the token"""
        if self.found:
            with open(self.dir + "\words.txt", "rb") as words:
                for i, line in enumerate(words):
                    if line.decode('utf8')==token+"\n":
                        return self.readDataFile(i)
                return []

    def readDataFile(self,i):
        arr=[]
        with open(self.dir + "\data.txt", "rb") as data:
            for idx, line in enumerate(data):
                if idx==i*2:
                    arr=decode(line)
                elif idx==(i*2)+1:
                    arr+=decode(line)
                elif idx>i*2:
                    break
        return arr

    def __init__(self, dir):
        """Creates an IndexReader which will read from
        the given directory"""
        self.found = False
        self.dir=dir
        if os.path.isdir(dir):
            if os.path.isfile(dir+"/Index.txt"):
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
        if reviewId==0:
            return -1
        with open(self.dir + "\TotalFreq.txt", "rb") as freq:
            for i, line in enumerate(freq):
                if i==reviewId:
                    return int(line.decode('utf8'))
        return -1

    def getTokenFrequency(self, token):
        """Return the number of reviews containing a
        given token (i.e., word)
        Returns 0 if there are no reviews containing
        this token"""
        return int(len(self.readWordsFile(token))/2)-1

    def getTokenCollectionFrequency(self, token):
        """Return the number of times that a given
        token (i.e., word) appears in
        the reviews indexed
        Returns 0 if there are no reviews containing
        this token"""
        arr=self.readWordsFile(token)
        arr=arr[int(len(arr)/2):]
        count=0
        for item in arr :
            count+=item
        return count

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
        str=[]
        ids=self.readWordsFile(token)
        freq= ids[int(len(ids)/2):]
        ids=ids[:int(len(ids)/2)]
        if len(ids)!=len(freq):
            return "there is a mistake in the arrays"
        else:
            for i,item in enumerate(ids):
                str.append(item)
                str.append(freq[i])
                # str+=self.get_reviews_with_token_text(item,freq[i])
                # if i!=len(ids)-1:
                #     str+=","
            return tuple(str)

    def getNumberOfReviews(self):
        """Return the number of product reviews
        available in the system"""
        return self.readIndexFile("ReviewsNum",0,0)+1

    def getTokenSizeOfReviews(self):
        """Return the number of tokens in the system
        (Tokens should be counted as many times as they
        appear)"""
        with open(self.dir + "\TotalFreq.txt", "rb") as total:
            for line in total:
                num=decode(line)
                break

        return num[0]

    def getProductReviews(self, productId):
        """Return the ids of the reviews for a given
        product identifier
        Note that the integers returned should be
        sorted by id
        Returns an empty Tuple if there are no reviews
        for this product"""
        ids=[]
        if self.found:
            with open(self.dir + "\index.txt", "rb") as data:
                for i, line in enumerate(data):
                    id = decode(line)
                    datatoreturn = ''.join(chr(i) for i in id[:self.productIdLen])
                    if datatoreturn==productId:
                        ids.append(i)
        return tuple(ids)


dir = "../projectSheltot"



reader=IndexReader(dir)
print(reader.getTokenSizeOfReviews())
