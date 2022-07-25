# JPM_Twitter_Relabelling

## Overcomplicated Sampling Methodology: 

### STEP 1: Filter through the users <br>

Users will be labelled as B-PER for now because most of the time @ tags reference people


### STEP 2: Filter through the rest of the tweets

#### Step 2a: If there is a hashtag, remove the hastag.

#### Then, break the combined hashtag word into multiple words

#### Run it through the WordNinja, which uses the Viterbo probability to split up the words

#### Then use Spacy to get the entities of both the combined and split phrase

#### Look through the labels
Take a counter of the max labels, - that will be the final label

Key: 
If PERSON = B-PER

If FAC = B-LOC

If NORP = B-ORG <br>
If ORG = B-ORG

If PRODUCT = B-MISC <br>
If EVENT = B-MISC <br>
If WORK OF ART = B-MISC <br>
If LAW = B-MISC <br>
If LANGUAGE = B-MISC <br>
If DATE = B-MISC (because event) <br>
If TIME = B-MISC (because event) <br>
If ORDINAL = B-MISC (because event) <br>
If CARDINAL = B-MISC (because event) <br>

If MONEY = ‘O’ (unrelated) <br>
If QUANTITY = ‘O’ (unrelated) 


#### If there is no labe, look through the POS-taggings: <br>
If PROPN = B-MISCIf NOUN = B-MISC <br> 
Else if everything else = ‘O’


#### FINAL CATEGORIES for Tweebank
B-PER <br>
B-ORG <br>
B-LOC <br>
B-MISC
