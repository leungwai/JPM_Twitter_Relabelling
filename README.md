# JPM_Twitter_Relabelling

Overcomplicated Sampling Methodology: 

Look through the labels
Take a counter of the max labels, - that will be B-label

If PERSON = B-PER

If FAC = B-LOC

If NORP = B-ORG
If ORG = B-ORG

If PRODUCT = B-MISC
If EVENT = B-MISC
If WORK OF ART = B-MISC
If LAW = B-MISC
If LANGUAGE = B-MISC
If DATE = B-MISC (event)
If TIME = B-MISC (event) 
If ORDINAL = B-MISC (event)
If Cardinal = B-MISC (event)

If MONEY = ‘O’ (unrelated)
If QUANTITY = ‘O’ (unrelated) 


Else, look through the POS-taggings:
If PROPN = B-MISC If NOUN = B-MISC 
Else if everything else = ‘O’


FINAL CATEGORIES
B-PER
B-ORG
B-LOC
B-MISC
