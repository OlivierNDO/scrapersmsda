# Import Packages
#####################################################################
import vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer # Must be installed with pip - no conda install that I could find
from vaderSentiment import sentiment as vaderSentiment 
import numpy as np, pandas as pd

# Define Function
#####################################################################
def gen_polarity(twt_str_list):
    temp_list = []
    for twt in twt_str_list:
        sent_intens = SentimentIntensityAnalyzer()
        pol_scores = sent_intens.polarity_scores(twt)
        pol_tuple_df = pd.DataFrame.from_dict([pol_scores.items()])
        iter_df = pd.DataFrame({'neg': pol_tuple_df[0].apply(pd.Series)[1],
                                  'neu': pol_tuple_df[1].apply(pd.Series)[1],
                                  'pos': pol_tuple_df[2].apply(pd.Series)[1],
                                  'compound': pol_tuple_df[3].apply(pd.Series)[1]})
        temp_list.append(iter_df)
    output_df = pd.concat(temp_list, axis=0)
    return output_df

"""
Input list of strings, output dataframe with four sentiment scores.

Example:

# Intentionally Deceptive Sentiment
tricky_speech = ['The book was good, but the protagonists are uncompelling and the narrative is not great.',
                 'This was among the least wonderful experiences I have every had. The food was not good.',
                 'The dining experience was akin to ingesting garbage. I recommended it to my neighbors of whom I am least fond.',
                 'This is the least disappointing food I have had in Boerne.',
                 'This restaurant was the shit.']

try_function = gen_polarity(tricky_speech)
try_function

"""
