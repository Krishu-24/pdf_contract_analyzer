import fitz
import datetime
from datetime import date, time, datetime, timedelta
import os
dtoday=datetime.now()
print(dtoday.day)
print(dtoday.year)
print(dtoday.month)
months = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12
}
def expdate(l1):
    for i in range(len(l1)):
        if"/" in l1[i] or "-" in l1[i]:
            sep="/" if "/" in l1[i] else "-"
            parts=l1[i].split(sep)
            if len(parts)==3 and all (p.isdigit() for p in parts):
                p1,p2,p3=map(int,parts)
                if p1 > 31:
                    month , day, year = p1, p2, p3
                else:
                    day, month, year = p1, p2, p3
                return datetime(year, month, day)
        if l1[i].isdigit():
            day=l1[i]
            monthattr=l1[i+1].lower()
            year=l1[i+2]
            break
        else:
            continue
    if monthattr.isdigit()==False:
        month=months[monthattr]
    else:
        month=monthattr
    return datetime(int(year),int(month),int(day))

flag="not saved"
ogpath="C:/Users/krish/Desktop/Document1(1).pdf"
fname=os.path.basename(ogpath)
expiry_folder="C:/Users/krish/Desktop/expires"
nonexpiry_folder="C:/Users/krish/Desktop/not expire"
expirypath=os.path.join(expiry_folder,fname)
nonexpirypath=os.path.join(nonexpiry_folder,fname)
doc=fitz.open(ogpath)
for page in doc:
    text=page.get_text()
    print(text)
    words=text.split()
    for i,word in enumerate(words):
        if "expire" in word.lower():
            lineafter=words[i+1:i+11]
            print(lineafter)
            expdatefile=expdate(lineafter)
            dleft=(expdatefile-dtoday).days
            if dleft<100:
                doc.save(expirypath)
                print("days left:",dleft)
                flag="saved"
                break
    if flag!="saved":
        doc.save(nonexpirypath)
doc.close()








