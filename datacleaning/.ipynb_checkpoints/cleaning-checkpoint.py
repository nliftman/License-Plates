"""This module is run to go from the unique master evil
words doc to the master counts document which 
contains each word and its scores."""
#libraries
import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None
#load in csv
df = pd.read_csv('uniqueevilmasterdoc.csv')
#only want the no space bc gives us more options
df = pd.DataFrame(df['nospace'])
#start by removing . because they are rly hard to remove for some reason
dropped = df.drop([1206, 1364, 1365])
#remove @ and get 1593
cleaned_df = dropped[~dropped.nospace.str.contains("@")]
#remove - and get 1583
cleaned_df = cleaned_df[~cleaned_df.nospace.str.contains("-")]
#remove ! and get 1574
cleaned_df = cleaned_df[~cleaned_df.nospace.str.contains("!")]
#remove _ and get 1567
cleaned_df = cleaned_df[~cleaned_df.nospace.str.contains("_")]
#remove / and get 1567
cleaned_df = cleaned_df[~cleaned_df.nospace.str.contains("/")]
#remove & and get 1566
cleaned_df = cleaned_df[~cleaned_df.nospace.str.contains("&")]
#remove + and get 1558
cleaned_df = cleaned_df[~cleaned_df.nospace.str.contains('+', regex = False)]
#remove * and get 1487
cleaned_df = cleaned_df[~cleaned_df.nospace.str.contains("*", regex = False)]
#remove # and get 1486
cleaned_df = cleaned_df[~cleaned_df.nospace.str.contains("#")]
#remove ' and get 1479
cleaned_df = cleaned_df[~cleaned_df.nospace.str.contains("'")]
#remove . and get 1477
cleaned_df = cleaned_df[~cleaned_df.nospace.str.contains(".", regex = False)]

#adding some evil words
cleaned_df.loc[1629] = ["88"]
cleaned_df.loc[1630] = ["fk"]
cleaned_df.loc[1631] = ["fkr"]
cleaned_df.loc[1632] = ["fker"]
cleaned_df.loc[1633] = ["1488"]
cleaned_df.loc[1634] = ["14"]
cleaned_df.loc[1635] = ["GTFO"]
cleaned_df.loc[1636] = ["H8"]
cleaned_df.loc[1637] = ["DGAF"]
cleaned_df.loc[1638] = ["LMAO"]
cleaned_df.loc[1639] = ["LMFAO"]
cleaned_df.loc[1640] = ["WTF"]
cleaned_df.loc[1641] = ["AK"]
cleaned_df.loc[1642] = ["AK47"]
cleaned_df.loc[1643] = ["gun"]
cleaned_df.loc[1644] = ["guns"]

#index is off so need to redo 
cleaned_df['row_num'] = range(0, len(cleaned_df))

#set the index as row_num
cleaned_df.set_index('row_num', inplace=True)

#load the big dataset
tweets = pd.read_csv('labeled_data.csv')
#remove class of 2
filt = tweets[tweets['class'] < 2]
#create hate speech and offensive language scores
filt['hate_score'] = filt['hate_speech']/filt['count']
filt['off_score'] = filt['offensive_language']/filt['count']

#create df of offensive words
off = pd.DataFrame(cleaned_df['nospace'])

#pull just the tweets
tweets = list(filt['tweet'])
#create the new coluns that we will iterate over
off['hate_speech'] = 1
off['offensive_language'] = 1
off['count_words'] = 1

#list of offensive words
off_words = list(off['nospace'])

#this gives us the count of each offensive word
for i, value in enumerate(off_words):
    count = sum(value in s for s in tweets)
    off['count_words'][i] = count

#this gives us the score
for i, value in enumerate(off_words):
    newdf = pd.DataFrame(filt[filt['tweet'].str.contains(value)])
    off['hate_speech'][i] = sum(newdf['hate_speech'])
    off['offensive_language'][i] = sum(newdf['offensive_language'])

#find out how many people ranked a tweet with this word in it
off['total_rating'] = off['hate_speech'] + off['offensive_language']
#find out what percent ranked it hate and offensive out of the total
off['hate_out_tot'] = off['hate_speech']/off['total_rating']
off['offense_out_tot'] = off['offensive_language']/off['total_rating']

#maximum count is 11151
off['count_perc'] = off['count_words']/11151
#get log
off['log_count'] = np.log(off['count_perc'])
off['pos_log'] = off['log_count'].abs()

#export df
off.to_csv('master_counts_scores.csv')