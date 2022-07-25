from reading_datasets import read_ud_dataset, reading_tb_ner
import pandas as pd

pos_train = read_ud_dataset(dataset = 'tb', location = '../Datasets/POSTagging/Tweebank/', split = 'train')
pos_val = read_ud_dataset(dataset = 'tb', location = '../Datasets/POSTagging/Tweebank/', split = 'dev')
pos_test = read_ud_dataset(dataset = 'tb', location = '../Datasets/POSTagging/Tweebank/', split = 'test')
ner_train = reading_tb_ner(location = '../Datasets/NER/Tweebank/', split = 'train')
ner_val = reading_tb_ner(location = '../Datasets/NER/Tweebank/', split = 'dev')
ner_test = reading_tb_ner(location = '../Datasets/NER/Tweebank/', split = 'test')

combined_dataset = []
for i, (tweet, pos_labels) in enumerate(pos_train):
    tweet = [token.lower() for token in tweet]
    query = ' '.join(tweet)

    found = False
    for ner_tweet, ner_labels in ner_train:
        ner_tweet = [token.lower() for token in ner_tweet]
        check = ' '.join(ner_tweet)
        if query == check:
            found = True
            break

    if found and tweet == ner_tweet:
        combined_dataset.append([tweet, pos_labels, ner_labels])

df = pd.DataFrame(columns = ['Word', 'POS Label', 'NER Label', 'Tweet'])

for tweet, pos_labels, ner_labels in combined_dataset:

    for t, p, n in zip(tweet, pos_labels, ner_labels):
        if p == 'PROPN' and n == 'O': #and t[0] != '@':
            df.loc[len(df.index)] = [t, p, n, ' '.join(tweet)]
            #print(t, '\t', p, '\t', n, '\t--> ', ' '.join(tweet) )


# Exporting it to a tsv file

df.to_csv('logs/combined_final.tsv', sep='\t', index=False)

print("Data combined and processed into tsv file")