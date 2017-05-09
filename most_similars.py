from gensim.models import Doc2Vec as d2v
from gensim.models import doc2vec
import gensim
import os
import collections
import smart_open
import random
import logging
from pdb import set_trace as st

def read_corpus(fname, tokens_only=False, pp=False):
    with smart_open.smart_open(fname, encoding="iso-8859-1") as f:
        for i, line in enumerate(f):
            if tokens_only:
                yield gensim.utils.simple_preprocess(line)
            else:
                # For training data, add tags
                if pp: # Preprocess strings
                    yield doc2vec.TaggedDocument(gensim.utils.simple_preprocess(line), 
                                              [i])
                else:  # Raw strings
                    yield doc2vec.TaggedDocument(line, [i])

# Logging all our program
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)
train=False
train_file="/almac/ignacio/data/GUsDany/corpus/GUs_literature.txt" #"/almac/ignacio/data/GUsDany/corpus/GUs_textform.txt"
dims=300
win=5
arch=1 #"cbow" && "skipgram" = 1; "skipgram"=0
model_file="/almac/ignacio/data/GUsDany/d2v_raw_GUs-literature-wiki_H%d_W%d_A%s.model" % (dims, win, arch)
centers=[int(i)-1 for i in "180,15,5".split(",")]
top=10


if train:
    train_corpus = list(read_corpus(train_file))

    model = d2v(size=dims, window=win, dbow_words=arch, min_count=1)
    model.build_vocab(train_corpus)
    model.train(train_corpus, total_examples=model.corpus_count)
    model.save(model_file)

m = d2v.load(model_file)
    
with open(train_file) as f0:
   GUs=f0.readlines()
   for gu_idx in centers:
       gu_similarities=m.docvecs.most_similar(gu_idx, topn=top)
       line=GUs[gu_idx]
       with open("rank_%s" % ''.join(line[0:15].strip().split()), "w") as f:
          f.write("# The most similars to this GU: '\n# %s'\n\n" % (line[0:70]))
          for sim in gu_similarities:
              f.write("%d\t%.5f\t%s\n" % (sim[0], sim[1], GUs[sim[0]][0:80]))  

