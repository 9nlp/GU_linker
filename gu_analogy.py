import multiprocessing
from argparse import ArgumentParser as ap
from gensim.models.keyedvectors import KeyedVectors as kv
#from gensim.models import Word2Vec as kv
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#n_cpus = 20
class corpus_streamer(object):
    """ This Object streams the input raw text file row by row. The constructor
    allows for streaming a dictionary (object), strings (True), lists (by space
    or any character) and sublists of strings (position='a:b') or a substring
    from the list in a specific position (position=index).
    """
    def __init__(self, file_name, dictionary=None, strings=None,
                                                    spliter="", position=":"):
        self.file_name=file_name
        self.dictionary=dictionary
        self.strings=strings
        self.spliter=spliter
        self.position=position
    def __iter__(self):
        for line in open(self.file_name):
        # assume there's one document per line, tokens separated by whitespace
            if self.dictionary and not self.strings:
                yield self.dictionary.doc2bow(line.lower().split())
            elif not self.dictionary and self.strings:
                if self.spliter=="":
                    yield line.strip()
                elif self.position==":" and self.spliter!="":
                    yield line.strip().split(self.spliter)
                elif not isinstance(self.position, int) and len(self.position)>1:
                    i,f=map(int, self.position.split(":"))
                    yield line.strip().split(self.spliter)[i:f]
                elif isinstance(self.position, int):
                    yield line.strip().split(self.spliter)[self.position]

def yield_results(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip().split()[4]

def check_analogy(analogy):
    # Verify the presence of a header
    if analogy.startswith(": "):
        return analogy

    words_analogy=analogy.split()
    try:
        Rs=we_model.most_similar_cosmul(positive=words_analogy[0:2], 
                                    negative=[words_analogy[2]], 
                                    topn=thr)
    except:
    # Return an erroneous analogy if some word is not in the 
    # vocabulary (this could be avoided by inferring word vector 
    # for fastext).
        return analogy + " error" 

    if words_analogy[3] in [r[0] for r in Rs]:
        return analogy + " correct"
    else:
        return analogy + " error"

def mp_handler(inlines=None, outfile = 'answers.txt'):
    global thr
    p = multiprocessing.Pool(thr)
    analogies=corpus_streamer(inlines, strings=True)
    #with open(inlines) as f:
        #analogies = [line for line in (l.strip() for l in f) if not line.startswith(": ")]
        #analogies=(l.strip() for l in f)
    with open(outfile, 'w') as f:
        for result in p.imap(check_analogy, analogies):
            f.write('%s\n' % result.encode('utf-8'))
    
if __name__=='__main__':

    parser = ap(description='This script computes the word analogy accuracy tests for word emebddings in an efficient way.')
    parser.add_argument("--inlines", help="A file containing lines to clean be evaluated (word analogies).", metavar="inlines",default=None)
    parser.add_argument("--model", help="A file containing the word embeddings in text format (vec).", metavar="model", required=True)
    parser.add_argument("--thr", help="The max number of answers given by the model to consider a correct answer.", metavar="thr",type=int)
    parser.add_argument("--outfile", help="A file where computed accuracies and analogies must be saved.", metavar="outfile", default="accuracies")
    args = parser.parse_args()

    global thr
    thr=args.thr

    print('\nLoading embeddings... pleace take a coffe...\n')

    we_model=kv.load_word2vec_format(args.model, 
                                         binary=False, 
                                         encoding='latin-1')

    mp_handler(args.inlines, args.outfile)
    
    corr=0
    eror=0
    c=0;x=""
    for r in yield_results(args.outfile):
        if r=="correct":
            corr+=1
            c+=1
        elif r=="error":
            eror+=1
            c+=1
        elif r.startswith(": "):
            
            if c:
            
                print (x)
                print('\nAccuracy for given word embeddings: %f  %% (%d / %d)' % (float(corr)/float(corr+eror), corr, eror))
            else: x=r

    print('\nAccuracy for given word embeddings: %f  %% (%d / %d)' % (float(corr)/float(corr+eror), corr, eror))
