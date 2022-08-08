from reading_datasets import read_ud_dataset, reading_tb_ner
import pandas as pd

pos_train = read_ud_dataset(dataset = 'tb', location = '../Datasets/POSTagging/Tweebank/', split = 'train')
pos_val = read_ud_dataset(dataset = 'tb', location = '../Datasets/POSTagging/Tweebank/', split = 'dev')
pos_test = read_ud_dataset(dataset = 'tb', location = '../Datasets/POSTagging/Tweebank/', split = 'test')
ner_train = reading_tb_ner(location = '../Datasets/NER/Tweebank/', split = 'train')
ner_val = reading_tb_ner(location = '../Datasets/NER/Tweebank/', split = 'dev')
ner_test = reading_tb_ner(location = '../Datasets/NER/Tweebank/', split = 'test')

#Getting all the tweets for training dataset
combined_dataset_train = []
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
        combined_dataset_train.append([tweet, pos_labels, ner_labels])

#Getting all the tweets for validation dataset
combined_dataset_val = []
for i, (tweet, pos_labels) in enumerate(pos_val):
    tweet = [token.lower() for token in tweet]
    query = ' '.join(tweet)

    found = False
    for ner_tweet, ner_labels in ner_val:
        ner_tweet = [token.lower() for token in ner_tweet]
        check = ' '.join(ner_tweet)
        if query == check:
            found = True
            break

    if found and tweet == ner_tweet:
        combined_dataset_val.append([tweet, pos_labels, ner_labels])

#Getting all the tweets for testing dataset
combined_dataset_test = []
for i, (tweet, pos_labels) in enumerate(pos_test):
    tweet = [token.lower() for token in tweet]
    query = ' '.join(tweet)

    found = False
    for ner_tweet, ner_labels in ner_test:
        ner_tweet = [token.lower() for token in ner_tweet]
        check = ' '.join(ner_tweet)
        if query == check:
            found = True
            break

    if found and tweet == ner_tweet:
        combined_dataset_test.append([tweet, pos_labels, ner_labels])

# Setting up the dataframe to get the specific labels
train_df = pd.DataFrame(columns = ['Word', 'Start Word Index', 'End Word Index', 'POS Label', 'NER Label', 'Tweet', 'Tweet POS Labels', 'Tweet NER Labels'])
val_df = pd.DataFrame(columns = ['Word', 'Start Word Index', 'End Word Index', 'POS Label', 'NER Label', 'Tweet', 'Tweet POS Labels', 'Tweet NER Labels'])
test_df = pd.DataFrame(columns = ['Word', 'Start Word Index', 'End Word Index', 'POS Label', 'NER Label', 'Tweet', 'Tweet POS Labels', 'Tweet NER Labels'])

# FOR TRAINING
for tweet, pos_labels, ner_labels in combined_dataset_train:
    continued_phrase = False
    start_index = 0
    end_index = 0
    t_phrase = []
    p_phrase = []
    n_phrase = []

    #DEBUGGING 
    # print("-" * 50)
    # print("TWEET")
    # print(tweet)
    # print("POS LABELS FOR SENTENCE")
    # print(pos_labels)
    # print("NER LABELS FOR SENTENCE")
    # print(ner_labels)
    
    for t, t_index, p, n in zip(tweet, range(len(tweet)), pos_labels, ner_labels):
        # start of phrase
        if (p == 'PROPN' and n == 'O' and continued_phrase == False): #and t[0] != '@':
            # if the phrase word in the phrase is @user
            if '@user' in t:
                train_df.loc[len(train_df.index)] = [t, t_index, t_index, p, n, ' '.join(tweet), pos_labels, ner_labels]
                continued_phrase == False
            else:
                continued_phrase = True
                start_index = t_index
                end_index = t_index
                t_phrase.append(t)
                p_phrase.append(p)
                n_phrase.append(n)
        
        # mid phrase
        elif (p == 'PROPN' and n == 'O' and continued_phrase == True): #and t[0] != '@':
         
            if '@user' in t:
                # save the phrase before the user tag first
                train_df.loc[len(train_df.index)] = [' '.join(t_phrase), start_index, end_index, p_phrase, n_phrase, ' '.join(tweet), pos_labels, ner_labels]
                
                # clear the list phrase
                combined_phrase = False
                start_index = 0
                end_index = 0
                t_phrase = []
                p_phrase = []
                n_phrase = []
                
                # add the current user tag 
                train_df.loc[len(train_df.index)] = [t, t_index, t_index, p, n, ' '.join(tweet), pos_labels, ner_labels]
            
            else:
                continued_phrase = True
                end_index = t_index
                t_phrase.append(t)
                p_phrase.append(p)
                n_phrase.append(n)

        # phrase ended or phrase has reached the end of sentence
        elif (continued_phrase == True) or (p == 'PROPN' and n == 'O' and continued_phrase == True and t_index == (len(tweet) - 1)):
            # breaks the cycle/phrase check or if reached end of sentence
            continued_phrase = False; 
            train_df.loc[len(train_df.index)] = [' '.join(t_phrase), start_index, end_index, p_phrase, n_phrase, ' '.join(tweet), pos_labels, ner_labels]
            
            start_index = 0
            end_index = 0
            t_phrase = []
            p_phrase = []
            n_phrase = []



# FOR VALIDATION
for tweet, pos_labels, ner_labels in combined_dataset_val:
    continued_phrase = False
    start_index = 0
    end_index = 0
    t_phrase = []
    p_phrase = []
    n_phrase = []

    #DEBUGGING 
    # print("-" * 50)
    # print("TWEET")
    # print(tweet)
    # print("POS LABELS FOR SENTENCE")
    # print(pos_labels)
    # print("NER LABELS FOR SENTENCE")
    # print(ner_labels)
    
    for t, t_index, p, n in zip(tweet, range(len(tweet)), pos_labels, ner_labels):
        # start of phrase
        if (p == 'PROPN' and n == 'O' and continued_phrase == False): #and t[0] != '@':
            # if the phrase word in the phrase is @user
            if '@user' in t:
                val_df.loc[len(val_df.index)] = [t, t_index, t_index, p, n, ' '.join(tweet), pos_labels, ner_labels]
                continued_phrase == False
            else:
                continued_phrase = True
                start_index = t_index
                end_index = t_index
                t_phrase.append(t)
                p_phrase.append(p)
                n_phrase.append(n)
        
        # mid phrase
        elif (p == 'PROPN' and n == 'O' and continued_phrase == True): #and t[0] != '@':
         
            if '@user' in t:
                # save the phrase before the user tag first
                val_df.loc[len(val_df.index)] = [' '.join(t_phrase), start_index, end_index, p_phrase, n_phrase, ' '.join(tweet), pos_labels, ner_labels]
                
                # clear the list phrase
                combined_phrase = False
                start_index = 0
                end_index = 0
                t_phrase = []
                p_phrase = []
                n_phrase = []
                
                # add the current user tag 
                val_df.loc[len(val_df.index)] = [t, t_index, t_index, p, n, ' '.join(tweet), pos_labels, ner_labels]
            
            else:
                continued_phrase = True
                end_index = t_index
                t_phrase.append(t)
                p_phrase.append(p)
                n_phrase.append(n)

        # phrase ended or phrase has reached the end of sentence
        elif (continued_phrase == True) or (p == 'PROPN' and n == 'O' and continued_phrase == True and t_index == (len(tweet) - 1)):
            # breaks the cycle/phrase check or if reached end of sentence
            continued_phrase = False; 
            val_df.loc[len(val_df.index)] = [' '.join(t_phrase), start_index, end_index, p_phrase, n_phrase, ' '.join(tweet), pos_labels, ner_labels]
            
            start_index = 0
            end_index = 0
            t_phrase = []
            p_phrase = []
            n_phrase = []


# FOR TESTING
for tweet, pos_labels, ner_labels in combined_dataset_test:
    continued_phrase = False
    start_index = 0
    end_index = 0
    t_phrase = []
    p_phrase = []
    n_phrase = []

    #DEBUGGING 
    # print("-" * 50)
    # print("TWEET")
    # print(tweet)
    # print("POS LABELS FOR SENTENCE")
    # print(pos_labels)
    # print("NER LABELS FOR SENTENCE")
    # print(ner_labels)
    
    for t, t_index, p, n in zip(tweet, range(len(tweet)), pos_labels, ner_labels):
        # start of phrase
        if (p == 'PROPN' and n == 'O' and continued_phrase == False): #and t[0] != '@':
            # if the phrase word in the phrase is @user
            if '@user' in t:
                test_df.loc[len(test_df.index)] = [t, t_index, t_index, p, n, ' '.join(tweet), pos_labels, ner_labels]
                continued_phrase == False
            else:
                continued_phrase = True
                start_index = t_index
                end_index = t_index
                t_phrase.append(t)
                p_phrase.append(p)
                n_phrase.append(n)
        
        # mid phrase
        elif (p == 'PROPN' and n == 'O' and continued_phrase == True): #and t[0] != '@':
         
            if '@user' in t:
                # save the phrase before the user tag first
                test_df.loc[len(test_df.index)] = [' '.join(t_phrase), start_index, end_index, p_phrase, n_phrase, ' '.join(tweet), pos_labels, ner_labels]
                
                # clear the list phrase
                combined_phrase = False
                start_index = 0
                end_index = 0
                t_phrase = []
                p_phrase = []
                n_phrase = []
                
                # add the current user tag 
                test_df.loc[len(test_df.index)] = [t, t_index, t_index, p, n, ' '.join(tweet), pos_labels, ner_labels]
            
            else:
                continued_phrase = True
                end_index = t_index
                t_phrase.append(t)
                p_phrase.append(p)
                n_phrase.append(n)

        # phrase ended or phrase has reached the end of sentence
        elif (continued_phrase == True) or (p == 'PROPN' and n == 'O' and continued_phrase == True and t_index == (len(tweet) - 1)):
            # breaks the cycle/phrase check or if reached end of sentence
            continued_phrase = False; 
            test_df.loc[len(test_df.index)] = [' '.join(t_phrase), start_index, end_index, p_phrase, n_phrase, ' '.join(tweet), pos_labels, ner_labels]
            
            start_index = 0
            end_index = 0
            t_phrase = []
            p_phrase = []
            n_phrase = []

#Exporting it to a tsv file

train_df.to_csv('logs/combined_train_final.tsv', sep='\t', index=False)
val_df.to_csv('logs/combined_val_final.tsv', sep='\t', index=False)
test_df.to_csv('logs/combined_test_final.tsv', sep='\t', index=False)

print("Data combined and processed into tsv file")