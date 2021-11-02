from typing import Text, List

import pandas as pd


def load_data(path: Text) -> List[Text]:
    """
    Function for loading data

    Args:
        data_path: the path to the data to be loaded
    
    Returns:
        data: list of sentences in data
    """

    with open(path, "r", encoding="utf8") as f:
        data = f.readlines()
    
    return data


def build_vocab_character(data, return_dataset=False):
    """
    Function for building character vocabulary 

    Args:
        data: list of sentences 
    
    Returns:
        charac2idx: dictionary character to index {'character':index}
    """

    corpus = []
    sents, labels = [], []

    for line in data:
        # Split data into original sentence and name+label
        splitted_sentence = line.split('\t')
        
        sentence = splitted_sentence[0]

        # Get name entity(lower)
        lowered_name = splitted_sentence[1][:splitted_sentence[1].find('|')]
        
        # Replace name entity(lower) in original sentence by name entity(upper)
        capitalized_sentence = sentence.replace(lowered_name, lowered_name.title())
        
        # Build corpus for character Vietnamese
        corpus.extend(list(capitalized_sentence))  

        sents.append(splitted_sentence[0])
        labels.append(splitted_sentence[1])

    # Build vocabulary for Vietnamese
    corpus =  pd.Series(corpus)
    vocab = corpus.unique()
    
    # Build dictionary character Vietnamese to index {'character':index}
    charac2idx = {w : i + 2 for i, w in enumerate(vocab)}
    charac2idx["UNK"] = 1
    charac2idx["PAD"] = 0
    
    if return_dataset:
        return charac2idx, (sents, labels)

    return charac2idx
