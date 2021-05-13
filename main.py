import benepar
import nltk
import pandas as pd
import re
import statistics
import spacy
import benepar
from scipy.stats import sem

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
benepar.download("benepar_en3")

spacy_parser = spacy.load("en_core_web_sm")
spacy_parser.add_pipe("benepar", config={"model": "benepar_en3"})

# load datasets from csv files
wsb = pd.read_csv(r"wsb.csv")
ssb = pd.read_csv(r"ssb.csv")
crypto = pd.read_csv(r"crypto.csv")
stocks = pd.read_csv(r"stocks.csv")

ds = pd.concat([wsb, stocks, crypto, ssb], axis=0)


def remove_emojis(sentence):
    pattern = re.compile("["
                         u"\U0001F600-\U0001F64F"  # emoticons
                         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                         u"\U0001F680-\U0001F6FF"  # transport & map symbols
                         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                         u"\U00002702-\U000027B0"
                         u"\U000024C2-\U0001F251"
                         "]+", flags=re.UNICODE)

    return pattern.sub(r"", sentence)


# filter emojis out from set
ds["body"] = ds["body"].apply(remove_emojis)

# tokenize into words and sentences
ds["words"] = ds["body"].apply(nltk.word_tokenize)
ds["sent"] = ds["body"].apply(nltk.sent_tokenize)

# tag pos
ds["pos"] = ds["words"].apply(nltk.pos_tag)


def parse_alphas(list):
    new_list = []
    for word in list:
        if word[0].isalpha():
            new_list.append((word[0].lower(), word[1]))
    return new_list


ds["pos"] = ds["pos"].apply(parse_alphas)

# for each set, calculate TTR, avg word len, avg sent len, clause/sentence, POS counts
sets = ["SatoshiStreetBets", "CryptoCurrency", "wallstreetbets", "stocks"]
word_lens = {}
sent_lens = {}
ttrs = {}
clause_sents = {}
pos_counts = {}
for s in sets:
    # avg word and sent len
    set_tokens = ds.loc[ds["subreddit"] == s]
    word_lengths = []
    sent_lengths = []
    ttr = []
    clause_per_sentence = []
    pos_ratio = {"nouns": [], "verbs": [], "adjectives": [], "adverbs": [], "total": []}
    for prog, row in set_tokens.iterrows():
        for w in row["words"]:
            word_lengths.append(len(w))

        for sen in row["sent"]:
            sent_length = len(re.findall(r"\w+", sen))
            sent_lengths.append(sent_length)

        tokens = row["pos"]
        wt = [t[0] for t in tokens]
        numtokens = len(wt)
        types = sorted(set(wt))
        numtypes = len(types)
        if numtypes > 0 and numtokens > 0:
            ttr.append(float(numtypes) / numtokens)

        nouns = 0
        verbs = 0
        adverbs = 0
        adjectives = 0
        total = len(row["pos"])
        for t in row["pos"]:
            if t[1] in ["NN", "NNS", "NNP", "NNPS"]:
                nouns += 1
            elif t[1] in ["VB", "VBD", "VBN", "VBP"]:
                verbs += 1
            elif t[1] in ["RB", "RBR", "RBS"]:
                adverbs += 1
            elif t[1] in ["JJ", "JJR", "JJS"]:
                adjectives += 1

        pos_ratio["nouns"].append(nouns)
        pos_ratio["verbs"].append(verbs)
        pos_ratio["adjectives"].append(adjectives)
        pos_ratio["adverbs"].append(adverbs)
        pos_ratio["total"].append(total)

        doc = spacy_parser(row["body"])
        if len(list(doc.sents)) > 0:
            spacy_sents = list(doc.sents)[0]
            # count number of S clauses in each sentence and add it to list
            clause_per_sentence.append(len(re.findall(r'\(S ', spacy_sents._.parse_string)))

        print(prog)

    word_lens[s] = (statistics.mean(word_lengths), sem(word_lengths))
    sent_lens[s] = (statistics.mean(sent_lengths), sem(sent_lengths))
    ttrs[s] = (statistics.mean(ttr), sem(ttr))
    clause_sents[s] = (statistics.mean(clause_per_sentence), sem(clause_per_sentence))
    pos_counts[s] = {"nouns": (statistics.mean(pos_ratio["nouns"]) / statistics.mean(pos_ratio["total"])),
                     "verbs": (statistics.mean(pos_ratio["verbs"]) / statistics.mean(pos_ratio["total"])),
                     "adjectives": (statistics.mean(pos_ratio["adjectives"]) / statistics.mean(pos_ratio["total"])),
                     "adverbs": (statistics.mean(pos_ratio["adverbs"]) / statistics.mean(pos_ratio["total"])),
                     "total": (statistics.mean(pos_ratio["total"]) / statistics.mean(pos_ratio["total"]))}

print("word lens", word_lens)
print("sent lens", sent_lens)
print("TTR", ttrs)
print("clause/sent", clause_sents)
print("pos counts", pos_counts)
