import spacy
import re
from dateutil import parser
#preprocessing text to remove ordinals
text=("This agreement is made between AlphaTech Pvt. Ltd. and Mr. Rajesh Kumar for IT consulting services. "
          "The agreement starts on March 10, 2024, and expires on March 10, 2025. "
          "Contract between GreenField Agro and Sunlight Logistics valid from January 5, 2023, to January 5, 2024. "
          "Service agreement: Emily Solutions will provide graphic design support to Flora & Co. for a period of 12 months beginning July 1, 2023. "
          "Contract ends on June 30, 2024. Agreement: Effective date – October 15, 2023. This contract is valid until October 15, 2024. "
          "License contract between Blue Ocean Corp. and Mr. David Lee. Valid from 12/04/2023 to 12/04/2025. "
          "Partnership agreement: begins on February 28, 2023, and terminates on February 28, 2026. "
          "Consulting contract executed on 01-11-2022 and will remain effective until 01-11-2023. "
          "Rental agreement: Start date – 2024-06-01. End date – 2025-05-31. "
          "Employment contract effective from 5th September 2022 and expiring on 5th September 2023. "
          "Maintenance contract entered into on April 1st, 2023, and shall expire on March 31st, 2024.")
norm_text=re.sub(r'(\d+)(st|nd|rd|th)', r'\1', text)
nlp = spacy.load("en_core_web_sm")
exp_sim_list = ["expire", "end", "valid", "terminate"]
exp_date=""
doc = nlp(norm_text)

for token in doc:
    if token.lemma_ in exp_sim_list:
        sub_sent = " ".join([t.text for t in token.subtree])
        print(sub_sent)
        sub_sent_wordlist=list(token.subtree)
        span=doc[sub_sent_wordlist[0].i:sub_sent_wordlist[-1].i+1]
        for tok in span.ents:
            if tok.label_=="DATE":
                print(tok)
                exp_date=tok.text
        print("final found exp_date=",exp_date)
        dt = parser.parse(exp_date)
        print(dt)
        print("\n")
        
