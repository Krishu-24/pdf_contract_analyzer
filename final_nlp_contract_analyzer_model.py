import spacy
import re
import numpy as np
import fitz
import datetime
from datetime import date, time, datetime, timedelta
import os
from dateutil import parser

days_before_expire=3 #specify the number of days to consider as expiring soon

ogpath="C:/Users/krish/Desktop/Document1(1).pdf" #file path 
expiry_folder="C:/Users/krish/Desktop/expires" #epiry folder path
nonexpiry_folder="C:/Users/krish/Desktop/not expire" #non expiry folder path
no_exp_date="" #folder to save for no expiration date

fname=os.path.basename(ogpath)
expirypath=os.path.join(expiry_folder,fname)
nonexpirypath=os.path.join(nonexpiry_folder,fname)
pdf=fitz.open(ogpath)

flag="not saved" #flag for saving the file

dtoday=datetime.now()

# print(dtoday.day)
# print(dtoday.year)
# print(dtoday.month)

nlp = spacy.load("en_core_web_md")
exp_sim_list = ["expire", "end", "valid", "terminate"] #list containing words similar to expire 

for page in pdf:
    text=page.get_text()
    #preprocessing text to remove ordinals
    norm_text=re.sub(r'(\d+)(st|nd|rd|th)', r'\1', text) 

    final_simlist=[] #list containing words similar to all words given inside above list to check for in document

    exp_date=""
    #adding similar words to final list
    for your_word in exp_sim_list: 
        ms = nlp.vocab.vectors.most_similar(np.asarray([nlp.vocab.vectors[nlp.vocab.strings[your_word]]]), n=20)
        words_list = [nlp.vocab.strings[w] for w in ms[0][0]]
        final_simlist.extend(words_list)
        print("searching for words: ",final_simlist)
    #reading and extracting tokens and recognizing date entities
    doc = nlp(norm_text)
    for token in doc:
        try:
            if token.lemma_ in final_simlist: #finding word root in documents that matches the final list of words
                sub_sent = " ".join([t.text for t in token.subtree])
                sub_sent_wordlist=list(token.subtree)
                span=doc[sub_sent_wordlist[0].i:sub_sent_wordlist[-1].i+1]
                for tok in span.ents:
                    if tok.label_=="DATE":
                        exp_date=tok.text
                try:
                    dt = parser.parse(exp_date)
                    dleft=(dt-dtoday).days
                    print("todays date: ",dtoday)
                    print("expiry date: ",dt)
                    print("days left for this contract to expire: ",dleft)
                    #comparing dates and saving file
                    try:
                        if dleft<days_before_expire:
                            pdf.save(expirypath)
                            print("agreement about to expire soon")
                            flag="saved"
                            print("saved file",fname,"in expiry folder",expiry_folder)
                            break
                    except:
                        print("error saving file")
                        flag="saved"
                except:
                    print("error processing found date")
                    flag="saved"#so that no furher processing is done to the pdf
        except:
            print("no expiration date found.")
            pdf.save(no_exp_date)
            print("file",fname,"saved in no expiration dates found folder",no_exp_date)
    
    try:            
        if flag!="saved":
            pdf.save(nonexpirypath)
            print("pdf not expiring soon")
            print("saved file",fname,"in nonexpiry_folder",nonexpiry_folder)
    except:
        print("error saving file")
pdf.close()
