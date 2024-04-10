import pandas as pd

def dataframe_similarity(df1, df2):
    # Ensure both dataframes compare the same columns, sorted alphabetically
    if set(df1.columns) != set(df2.columns):
        return "Can't calculate Precision, Recall and F1. DataFrames must have the same columns"
    
    df1 = df1.sort_index(axis=1).reset_index(drop=True)
    df2 = df2.sort_index(axis=1).reset_index(drop=True)
    
    # Create tuples of the rows
    df1['combined'] = df1.apply(lambda row: tuple(row), axis=1)
    df2['combined'] = df2.apply(lambda row: tuple(row), axis=1)
    
    # Create sets of the tuple rows for fast comparison
    set_df1 = set(df1['combined'])
    set_df2 = set(df2['combined'])
    
    # True Positives (TP): Items in both sets
    tp = len(set_df1.intersection(set_df2))
    
    # False Positives (FP): Items in df1 but not in df2
    fp = len(set_df1 - set_df2)
    
    # False Negatives (FN): Items in df2 but not in df1
    fn = len(set_df2 - set_df1)
    
    # Calculating precision, recall, and F1-score
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {'prec':round(precision,3), 'rec':round(recall,3), 'f1':round(f1,3)}