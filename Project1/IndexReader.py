from __future__ import division
import re
import pickle
import os
import binascii
from io import BytesIO
import sys

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

class IndexReader:

    def readIndexFile(self,type,reviewId,nullreturn):
        datatoreturn=nullreturn
        if self.found:
            with open(self.dir + "\index.txt", "rb") as data:

                for i, line in enumerate(data):
                    if reviewId - 1 == i:
                        id = decode(line)
                        count = 0
                        for idx, item in enumerate(id):
                            if item == 47:
                                count = idx
                                break
                        if type=="score":
                            datatoreturn=id[2*count+1+self.productIdLen]
                            break
                        elif type=="id":
                            datatoreturn= ''.join(chr(i) for i in id[2*count+1:2*count+1+self.productIdLen])
                            break
                        elif type=="numerator":
                            datatoreturn = int(''.join(chr(i) for i in id[0:count]))
                            #datatoreturn=int(chr(id[self.productIdLen:length]))
                        elif type=="denominator":
                            length = int((len(id) - self.productIdLen - 1) / 2) + self.productIdLen
                            datatoreturn = int(''.join(chr(i) for i in id[count+1:2*count+1]))
                        elif type=="length":
                            datatoreturn = id[2 * count + 1 + self.productIdLen+1]
                    elif reviewId - 1 < i:
                        break
        return datatoreturn

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
        return self.readIndexFile("length",reviewId,-1)

    def getTokenFrequency(self, token):
        """Return the number of reviews containing a
        given token (i.e., word)
        Returns 0 if there are no reviews containing
        this token"""
        if hasattr(self, 'data_dict'):
            count=0
            for i in range(int(len(self.data_dict))):
                if(token in self.data_dict[i+1]["text"]):
                    count+=1
            return count
    def getTokenCollectionFrequency(self, token):
        """Return the number of times that a given
        token (i.e., word) appears in
        the reviews indexed
        Returns 0 if there are no reviews containing
        this token"""
        count=0
        for i in range(int(len(self.data_dict))):
            my_str=self.data_dict[i+1]["text"]
            count+=my_str.count(token)
        return count

    def get_reviews_with_token_text(self,id,freq):
        return "id"+str(id)+", freq-"+str(freq)

    def getReviewsWithToken(self, token):
        """Returns a series of integers of the form id1, freq-1, id-2, freq-2, ... such
        that id-n is the n-th review containing the
        given token and freq-n is the
        number of times that the token appears in
        review id-n
        Note that the integers should be sorted by id
        Returns an empty Tuple if there are no reviews
        containing this token"""
        final_text=""
        for i in range(int(len(self.data_dict))):
            my_str = self.data_dict[i+1]["text"]
            freq = my_str.count(token)
            if freq != 0:
                final_text += self.get_reviews_with_token_text(i+1, freq)+", "
        if len(final_text) != 0:
            final_text = final_text[0:-2]

        return final_text

    def getNumberOfReviews(self):
        """Return the number of product reviews
        available in the system"""
        return len(self.data_dict)

    def getTokenSizeOfReviews(self):
        """Return the number of tokens in the system
        (Tokens should be counted as many times as they
        appear)"""
        count=0
        for i in range(int(len(self.data_dict))):
            my_str = self.data_dict[i + 1]["text"]
            count+=len(re.findall(r'\w+', my_str))
        return count

    def getProductReviews(self, productId):
        """Return the ids of the reviews for a given
        product identifier
        Note that the integers returned should be
        sorted by id
        Returns an empty Tuple if there are no reviews
        for this product"""
        ids=[]
        j=0
        for i in range(int(len(self.data_dict))):
            my_id = self.data_dict[i + 1]["product"]
            if my_id==productId:
                ids.append(i+1)
                j+=1
        return ids



dir = "../projectSheltot"


reader=IndexReader(dir)
print(reader.getReviewLength(100))
