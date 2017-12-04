# author: Shane Yu  date: April 8, 2017
# author: Chang Tai-Wei  date: April 8, 2017

class KEM(object):
    """
    KEM class uses MongoDB as a cache to accelerate the process of querying kem model,
    most_similar() function returns a list of query result from MongoDB if the query term exists in
    the database(fast), and only do the gensim built-in query function when the query term is not
    in the database(slow).
    """
    def __init__(self, uri, model_path = './med400.model.bin'):
        from ngram import NGram
        import gensim
        self.model = gensim.models.keyedvectors.KeyedVectors.load_word2vec_format(model_path, binary=True)

        # ngram search
        self.modelNgram = NGram(self.model.wv.vocab.keys())

    def most_similar(self, keyword, num):
        """
        input: keyword term of top n
        output: keyword result in json formmat
        """
        try:
            return self.model.most_similar(keyword, topn = num) # most_similar return a list
        except KeyError as e:
            keyword = self.modelNgram.find(keyword)
            if keyword:
                return self.model.most_similar(keyword, topn = num)
            return [('None', 0)]

    def getVect(self, keyword):
        try:
            return self.model[keyword].tolist()
        except KeyError as e:
            keyword = self.modelNgram.find(keyword)
            if keyword:
                return self.model[keyword].tolist()
            return [0]*400

if __name__ == '__main__':
    import json
    """
    due to the base directory settings of django, the model_path needs to be different when
    testing with this section.
    """
    import sys
    obj = KEM('mongodb://140.120.13.244:7777/', model_path = './med400.model.bin')
    temp = obj.most_similar(sys.argv[1], 100)
    print(temp)