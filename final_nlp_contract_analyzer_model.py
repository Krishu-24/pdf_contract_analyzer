import spacy
import re
import numpy as np
import fitz
import datetime
from datetime import date, time, datetime, timedelta
import os
from dateutil import parser
ogpath="C:/Users/krish/Desktop/Document1(1).pdf" #file path 
expiry_folder="C:/Users/krish/Desktop/expires" #epiry folder path
nonexpiry_folder="C:/Users/krish/Desktop/not expire" #non expiry folder path

fname=os.path.basename(ogpath)
expirypath=os.path.join(expiry_folder,fname)
nonexpirypath=os.path.join(nonexpiry_folder,fname)
pdf=fitz.open(ogpath)

flag="not saved"

dtoday=datetime.now()

# print(dtoday.day)
# print(dtoday.year)
# print(dtoday.month)

nlp = spacy.load("en_core_web_md")

for page in pdf:
    text=page.get_text()
    #preprocessing text to remove ordinals
    norm_text=re.sub(r'(\d+)(st|nd|rd|th)', r'\1', text)
    exp_sim_list = ["expire", "end", "valid", "terminate"]
    final_simlist=[]
    exp_date=""
    for your_word in exp_sim_list:
        ms = nlp.vocab.vectors.most_similar(np.asarray([nlp.vocab.vectors[nlp.vocab.strings[your_word]]]), n=20)
        words_list = [nlp.vocab.strings[w] for w in ms[0][0]]
        final_simlist.extend(words_list)
    doc = nlp(norm_text)
    for token in doc:
        if token.lemma_ in final_simlist:
            sub_sent = " ".join([t.text for t in token.subtree])
            # print(sub_sent)
            sub_sent_wordlist=list(token.subtree)
            span=doc[sub_sent_wordlist[0].i:sub_sent_wordlist[-1].i+1]
            for tok in span.ents:
                if tok.label_=="DATE":
                    # print(tok)
                    exp_date=tok.text
            # print("final found exp_date=",exp_date)
            dt = parser.parse(exp_date)
            # print(dt)
            # print("\n")
            dleft=(dt-dtoday).days
            if dleft<100:
                pdf.save(expirypath)
                # print("days left:",dleft)
                flag="saved"
                break
    if flag!="saved":
        pdf.save(nonexpirypath)
pdf.close()


print(words)
