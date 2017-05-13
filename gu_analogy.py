import multiprocessing
from argparse import ArgumentParser as ap
#from ast import literal_eval as le
from gensim.models.keyedvectors import KeyedVectors
#from gensim.models import Word2Vec
import logging
#load_vectors=vDB.load_word2vec_format

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
n_cpus = 20

def yield_results(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip().split()[4]

def check_analogy(analogy):
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
    p = multiprocessing.Pool(n_cpus)

    with open(inlines) as f:
        analogies = [line for line in (l.strip() for l in f) if not line.startswith(": ")]
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

    we_model=KeyedVectors.load_word2vec_format(args.model, 
                                         binary=False, 
                                         encoding='latin-1')

    mp_handler(args.inlines, args.outfile)
    
    corr=0
    eror=0
    for r in yield_results(args.outfile):
        if r=="correct":
            corr+=1
        elif r=="error":
            eror+=1

    print('\nAccuracy for given word embeddings: %f ' % (float(corr)/float(corr+eror)))
