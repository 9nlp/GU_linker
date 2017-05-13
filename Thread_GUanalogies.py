import threading
import Queue
import sys
import queue
from gensim.models.keyedvectors import KeyedVectors as kv
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class corpus_streamer(object):
    """ This Object streams the input raw text file row by row.
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
            if self.dictionary and not self.strings:
                yield self.dictionary.doc2bow(line.lower().split())
            elif not self.dictionary and self.strings:
                if self.spliter=="":
                    yield line.strip()
                elif self.position==":":
                    yield line.strip().split(self.spliter)

def do_work(analogy):
    if analogy.startswith(": "):
        return analogy

    words_analogy=analogy.split()
    try:
        Rs=we_model.most_similar_cosmul(positive=words_analogy[0:2],
                                negative=[words_analogy[2]],
                                topn=threshold)
        except:
# Return an erroneous analogy if some word is not in the
# vocabulary (this could be avoided by inferring word vector
# for fastext).
            return analogy + " error"

    if words_analogy[3] in [r[0] for r in Rs]:
        return analogy + " correct"
    else:
        return analogy + " error"

def worker():
    while True:
        analogy = q.get()
        if analogy is None:
            break
        do_work(analogy)
        q.task_done()

if __name__=='__main__':

    parser = ap(description='This script computes the word analogy accuracy tests for word emebddings in an efficient way.')
    parser.add_argument("--inlines", help="A file containing lines to clean be evaluated (word analogies).", metavar="inlines",default=None)
    parser.add_argument("--model", help="A file containing the word embeddings in text format (vec).", metavar="model", required=True)
    parser.add_argument("--threshold", help="The max number of answers given by the model to consider a correct answer.", metavar="threshold",type=int)
    parser.add_argument("--threads", help="Number of processing threads.", metavar="threads",type=int)
    parser.add_argument("--outfile", help="A file where computed accuracies and analogies must be saved.", metavar="outfile", default="accuracies")
    args = parser.parse_args()
    global threshold
    threshold=args.threshold
    nb_threads=args.threads

    print('\nLoading embeddings... pleace take a coffe...\n')

    word_analogies=corpus_streamer(args.inlines, strings=True)
    we_model=kv.load_word2vec_format(args.model,
                                         binary=False,
                                         encoding='latin-1')
    q = queue.Queue()
    threads = []
    for i in range(thr):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    for a in word_analogies:
        q.put(a)

# block until all tasks are done
    q.join()
# stop workers
    for i in range(nb_threads):
        q.put(None)
    for t in threads:
        t.join()
