from nltk.tokenize import word_tokenize

# input file
infile = "log.txt"

# fragment label before and after index
# Update for new sources
prologue = "maybridge_fragment_"
epilogue = ".pdbqt"

# pattern to catch affinities
# Should remain constant between sources, verification necessary
count_start = "u.b"
hit_one = 24
hit_inc = 4
hit_total = 10
hits = []
for i in range(hit_total):
    hits.append(hit_one + i * hit_inc)

# open file & get tokens
with open(infile) as fin:
    tokens = word_tokenize(fin.read())

# loop prep
affinities = []
start_cut = len(prologue)
end_cut = len(epilogue)
count = False
counter = 0
num = 0

frag_bests = []

for token in tokens:
    if count:  # Track progress to hits
        counter += 1
    if prologue in token:  # Update fragment number
        num = token[start_cut:-end_cut]
    elif token == count_start:  # Start count to hits
        count = True
    elif counter in hits:  # hit! save value
        affinities.append(float(token))
        if len(affinities) == hit_total:  # last hit for frag: output & reset
            best = (num,max(affinities))
            frag_bests.append(best)

            affinities.clear()
            counter = count = 0

frag_bests.sort(key=lambda tup: tup[1], reverse = True)

print(*frag_bests, sep="\n")
