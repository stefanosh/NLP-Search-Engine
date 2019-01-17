import json
from pprint import pprint

# for every article it removes the stopwords, by creating a new array which holds all the values of


def removeStopWords(data):
    closedClassCategoriesTuple = ("CD", "CC", "DT", "EX", "IN", "LS", "MD", "PDT",
                                  "POS", "PRP",  "PRP",  "RP",   "TO", "UH", "WDT", "WP", "WP", "WRB")

    dataToReturn = {"articles": []}
    for article in data["articles"]:  # for every article:
        for text_id in article:
            # for every word in every article
            for word in article[str(text_id)]:
                if word["pos_tag"] not in closedClassCategoriesTuple:  # if the tag isn't closedclass
                    # hold the word, either by creating value for text_id, or if text_id already exists, add it to its values
                    # so that we have same structure as file created after posTagging
                    for i in dataToReturn["articles"]:
                        if(str(text_id) in i):
                            dataToReturn["articles"][dataToReturn["articles"].index(
                                i)][str(text_id)].append(word)
                            break
                    else:
                        dataToReturn["articles"].append({str(text_id): [word]})

    return dataToReturn


with open('withpos.json') as f:
    data = json.load(f)

data = removeStopWords(data)
pprint(data)
