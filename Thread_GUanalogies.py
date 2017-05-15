from __future__ import print_function

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

def yield_results(filename):
    with open(filename) as f:
        for line in f:
            if line.startswith(": "):
                yield line.strip()
            elif line.startswith("# "):
                continue
            else:
                try:
                    yield line.strip().split()[4]
                except:
                    continue

def compute_results(results_file, append=False):
    results={}
    for r in yield_results(results_file):
        if r.startswith(": "):
            section=r[2:]
            results[section]=[0, 0]
        elif r.startswith("# "):
            continue
        else:
            if r=="correct":
                results[section][0]+=1
            elif r=="error":
                results[section][1]+=1

    if append:
        f=open(args.outfile, "a")
        print_r=f.write
    else:
        print_r=print

    print_r("\n")
    all_errors=[]
    all_correc=[]
    for section in results:
        corr=results[section][0]
        all_correc.append(corr)
        eror=results[section][1]
        all_errors.append(eror)
        print_r("Errors: %d\t Corrects: %d\tPrecision: %.4f %%\tSection: %s'\n" % 
                          (eror, corr, float(corr)/float(corr+eror), section))

    eror=sum(all_errors)
    corr=sum(all_correc)

    print_r("\nTotal errors: %d\t Total corrects: %d\tTotal precision: %.4f %%\n" %
                          (eror, corr, float(corr)/float(corr+eror)))

def do_work(analogy):
    global out_file
    if analogy.startswith(": "):
        out_file.write("%s\n"%analogy)
        return
    elif analogy.startswith("# "):
        return

    words_analogy=analogy.split()
    try:
        Rs=we_model.most_similar_cosmul(positive=words_analogy[0:2],
                                negative=[words_analogy[2]],
                                topn=threshold)
    except:
# Return an erroneous analogy if some word is not in the
# vocabulary (this could be avoided by inferring word vector
# for fastext).
        out_file.write(analogy + " error\n")
        return

    if words_analogy[3] in [r[0] for r in Rs]:
        out_file.write(analogy +  " correct\n")
    else:
        out_file.write(analogy + " error\n")

    return

def worker():
    while True:
        analogy = q.get()
        if analogy is None:
            break
        do_work(analogy)
        q.task_done()

if __name__=='__main__':
    from argparse import ArgumentParser as ap
    parser = ap(description='This script computes the word analogy accuracy tests for word emebddings in an efficient way.')
    parser.add_argument("--inlines", help="A file containing lines to clean be evaluated (word analogies).", metavar="inlines", required=True)
    parser.add_argument("--model", help="A file containing the word embeddings in text format (vec).", metavar="model", required=True)
    parser.add_argument("--threshold", help="The max number of answers given by the model to consider a correct answer (defualt=15).", metavar="threshold",type=int, default=15)
    parser.add_argument("--threads", help="Number of processing threads (default=5, more than this can lead to memory overload.).", metavar="threads",type=int, default=5)
    parser.add_argument("--outfile", help="A file where computed accuracies and analogies must be saved.", metavar="outfile", default="accuracies", required=True)
    args = parser.parse_args()
    global threshold
    threshold=args.threshold
    nb_threads=args.threads
    global out_file

    print('\nLoading embeddings... pleace take a coffe...\n')

    word_analogies=corpus_streamer(args.inlines, strings=True)
    we_model=kv.load_word2vec_format(args.model,
                                         binary=False,
                                         encoding='latin-1')
    q = queue.Queue()
    threads = []
    for i in range(nb_threads):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    out_file=open(args.outfile, "w")
    out_file.write("# Model: %s\n" % args.model)
    out_file.write("# Tolerance: %d\n"% args.threshold)
  
    for a in word_analogies:
        q.put(a)

    # block until all tasks are done
    q.join()
    # stop workers
    for i in range(nb_threads):
        q.put(None)
    for t in threads:
        t.join()

    out_file.close()
    
    compute_results(args.outfile, append=True)
