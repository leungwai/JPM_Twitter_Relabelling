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



#________________________________________
# FOR TRAINING
for tweet, pos_labels, ner_labels in combined_dataset_train:
    continued_phrase = False
    start_index = 0
    end_index = 0
    t_phrase = []
    p_phrase = []
    n_phrase = []

    
    for t, t_index, p, n in zip(tweet, range(len(tweet)), pos_labels, ner_labels):
        # if word match and word phrase not started
        if (p == 'PROPN' and n == 'O' and continued_phrase == False):
            
            # if the phrase word in the phrase is @user, split it up in its own separate tag
            if '@user' in t:
                train_df.loc[len(train_df.index)] = [t, t_index, t_index, [p], [n], ' '.join(tweet), pos_labels, ner_labels]
                continued_phrase == False
            
            # otherwise start a new phrase
            else:
                continued_phrase = True
                start_index = t_index
                end_index = t_index
                t_phrase.append(t)
                p_phrase.append(p)
                n_phrase.append(n)
        
        # else if word match during mid-phrase
        elif (p == 'PROPN' and n == 'O' and continued_phrase == True): #and t[0] != '@':
            
            # if usertag, then save the previous pattern, and save usertag as its own tag
            if '@user' in t:
                if t_phrase != []:
                    train_df.loc[len(train_df.index)] = [' '.join(t_phrase), start_index, end_index, p_phrase, n_phrase, ' '.join(tweet), pos_labels, ner_labels]
                
                # add the current user tag 
                train_df.loc[len(train_df.index)] = [t, t_index, t_index, [p], [n], ' '.join(tweet), pos_labels, ner_labels]

                # clear the list phrase
                combined_phrase = False
                start_index = 0
                end_index = 0
                t_phrase = []
                p_phrase = []
                n_phrase = []
            
            # else if the phrase is a hashtag, check if previous element is hashtag - if it is, break them into separate tags
            # if not, then continue a hashtag/non hashtag phrase 
            elif t[0:1] == '#':
                
                if t_phrase != []:
                    # check if the previous element is a hashtag
                    if t_phrase[len(t_phrase) - 1][0:1] == '#':
                        # add the previous phrase to the list
                        train_df.loc[len(train_df.index)] = [' '.join(t_phrase), start_index, end_index, p_phrase, n_phrase, ' '.join(tweet), pos_labels, ner_labels]

                        # reset the phrase
                        start_index = 0
                        end_index = 0
                        t_phrase = []
                        p_phrase = []
                        n_phrase = []

                        # start the new phrase with the hashtag
                        continued_phrase = True
                        start_index = t_index
                        end_index = t_index
                        t_phrase.append(t)
                        p_phrase.append(p)
                        n_phrase.append(n)

            # otherwise append word to existing phrase
            else:
                continued_phrase = True
                end_index = t_index
                t_phrase.append(t)
                p_phrase.append(p)
                n_phrase.append(n)

        # else if phrase ended or phrase has reached the end of sentence
        elif ((not (p == 'PROPN' and n == 'O')) and continued_phrase == True) or (p == 'PROPN' and n == 'O' and continued_phrase == True and t_index == (len(tweet)-1)):
            
            # if phrase is not empty, store the phrase in the list
            if t_phrase != []:
                train_df.loc[len(train_df.index)] = [' '.join(t_phrase), start_index, end_index, p_phrase, n_phrase, ' '.join(tweet), pos_labels, ner_labels]

            # prepare for new tweet (although it will reset in the top as well)
            continued_phrase = False
            start_index = 0
            end_index = 0
            t_phrase = []
            p_phrase = []
            n_phrase = []


#________________________________________
# FOR VALIDATION
for tweet, pos_labels, ner_labels in combined_dataset_val:
    continued_phrase = False
    start_index = 0
    end_index = 0
    t_phrase = []
    p_phrase = []
    n_phrase = []

    
    for t, t_index, p, n in zip(tweet, range(len(tweet)), pos_labels, ner_labels):
        # if word match and word phrase not started
        if (p == 'PROPN' and n == 'O' and continued_phrase == False):
            
            # if the phrase word in the phrase is @user, split it up in its own separate tag
            if '@user' in t:
                val_df.loc[len(val_df.index)] = [t, t_index, t_index, [p], [n], ' '.join(tweet), pos_labels, ner_labels]
                continued_phrase == False
            
            # otherwise start a new phrase
            else:
                continued_phrase = True
                start_index = t_index
                end_index = t_index
                t_phrase.append(t)
                p_phrase.append(p)
                n_phrase.append(n)
        
        # else if word match during mid-phrase
        elif (p == 'PROPN' and n == 'O' and continued_phrase == True): #and t[0] != '@':
            
            # if usertag, then save the previous pattern, and save usertag as its own tag
            if '@user' in t:
                if t_phrase != []:
                    val_df.loc[len(val_df.index)] = [' '.join(t_phrase), start_index, end_index, p_phrase, n_phrase, ' '.join(tweet), pos_labels, ner_labels]
                
                # add the current user tag 
                val_df.loc[len(val_df.index)] = [t, t_index, t_index, [p], [n], ' '.join(tweet), pos_labels, ner_labels]

                # clear the list phrase
                combined_phrase = False
                start_index = 0
                end_index = 0
                t_phrase = []
                p_phrase = []
                n_phrase = []
            
            # else if the phrase is a hashtag, check if previous element is hashtag - if it is, break them into separate tags
            # if not, then continue a hashtag/non hashtag phrase 
            elif t[0:1] == '#':
                
                if t_phrase != []:
                    # check if the previous element is a hashtag
                    if t_phrase[len(t_phrase) - 1][0:1] == '#':
                        # add the previous phrase to the list
                        val_df.loc[len(val_df.index)] = [' '.join(t_phrase), start_index, end_index, p_phrase, n_phrase, ' '.join(tweet), pos_labels, ner_labels]

                        # reset the phrase
                        start_index = 0
                        end_index = 0
                        t_phrase = []
                        p_phrase = []
                        n_phrase = []

                        # start the new phrase with the hashtag
                        continued_phrase = True
                        start_index = t_index
                        end_index = t_index
                        t_phrase.append(t)
                        p_phrase.append(p)
                        n_phrase.append(n)

            # otherwise append word to existing phrase
            else:
                continued_phrase = True
                end_index = t_index
                t_phrase.append(t)
                p_phrase.append(p)
                n_phrase.append(n)

        # else if phrase ended or phrase has reached the end of sentence
        elif ((not (p == 'PROPN' and n == 'O')) and continued_phrase == True) or (p == 'PROPN' and n == 'O' and continued_phrase == True and t_index == (len(tweet)-1)):
            
            # if phrase is not empty, store the phrase in the list
            if t_phrase != []:
                val_df.loc[len(val_df.index)] = [' '.join(t_phrase), start_index, end_index, p_phrase, n_phrase, ' '.join(tweet), pos_labels, ner_labels]

            # prepare for new tweet (although it will reset in the top as well)
            continued_phrase = False
            start_index = 0
            end_index = 0
            t_phrase = []
            p_phrase = []
            n_phrase = []
    

#________________________________________
# FOR TESTING
for tweet, pos_labels, ner_labels in combined_dataset_test:
    continued_phrase = False
    start_index = 0
    end_index = 0
    t_phrase = []
    p_phrase = []
    n_phrase = []

    
    for t, t_index, p, n in zip(tweet, range(len(tweet)), pos_labels, ner_labels):
        # if word match and word phrase not started
        if (p == 'PROPN' and n == 'O' and continued_phrase == False):
            
            # if the phrase word in the phrase is @user, split it up in its own separate tag
            if '@user' in t:
                test_df.loc[len(test_df.index)] = [t, t_index, t_index, [p], [n], ' '.join(tweet), pos_labels, ner_labels]
                continued_phrase == False
            
            # otherwise start a new phrase
            else:
                continued_phrase = True
                start_index = t_index
                end_index = t_index
                t_phrase.append(t)
                p_phrase.append(p)
                n_phrase.append(n)
        
        # else if word match during mid-phrase
        elif (p == 'PROPN' and n == 'O' and continued_phrase == True): #and t[0] != '@':
            
            # if usertag, then save the previous pattern, and save usertag as its own tag
            if '@user' in t:
                if t_phrase != []:
                    test_df.loc[len(test_df.index)] = [' '.join(t_phrase), start_index, end_index, p_phrase, n_phrase, ' '.join(tweet), pos_labels, ner_labels]
                
                # add the current user tag 
                test_df.loc[len(test_df.index)] = [t, t_index, t_index, [p], [n], ' '.join(tweet), pos_labels, ner_labels]

                # clear the list phrase
                combined_phrase = False
                start_index = 0
                end_index = 0
                t_phrase = []
                p_phrase = []
                n_phrase = []
            
            # else if the phrase is a hashtag, check if previous element is hashtag - if it is, break them into separate tags
            # if not, then continue a hashtag/non hashtag phrase 
            elif t[0:1] == '#':
                
                if t_phrase != []:
                    # check if the previous element is a hashtag
                    if t_phrase[len(t_phrase) - 1][0:1] == '#':
                        # add the previous phrase to the list
                        test_df.loc[len(test_df.index)] = [' '.join(t_phrase), start_index, end_index, p_phrase, n_phrase, ' '.join(tweet), pos_labels, ner_labels]

                        # reset the phrase
                        start_index = 0
                        end_index = 0
                        t_phrase = []
                        p_phrase = []
                        n_phrase = []

                        # start the new phrase with the hashtag
                        continued_phrase = True
                        start_index = t_index
                        end_index = t_index
                        t_phrase.append(t)
                        p_phrase.append(p)
                        n_phrase.append(n)

            # otherwise append word to existing phrase
            else:
                continued_phrase = True
                end_index = t_index
                t_phrase.append(t)
                p_phrase.append(p)
                n_phrase.append(n)

        # else if phrase ended or phrase has reached the end of sentence
        elif ((not (p == 'PROPN' and n == 'O')) and continued_phrase == True) or (p == 'PROPN' and n == 'O' and continued_phrase == True and t_index == (len(tweet)-1)):
            
            # if phrase is not empty, store the phrase in the list
            if t_phrase != []:
                test_df.loc[len(test_df.index)] = [' '.join(t_phrase), start_index, end_index, p_phrase, n_phrase, ' '.join(tweet), pos_labels, ner_labels]

            # prepare for new tweet (although it will reset in the top as well)
            continued_phrase = False
            start_index = 0
            end_index = 0
            t_phrase = []
            p_phrase = []
            n_phrase = []    

#Exporting it to a tsv file

train_df.to_csv('logs/combined_train_labels_FINAL.tsv', sep='\t', index=False)
val_df.to_csv('logs/combined_val_labels_FINAL.tsv', sep='\t', index=False)
test_df.to_csv('logs/combined_test_labels_FINAL.tsv', sep='\t', index=False)

print("Data combined and processed into tsv file")