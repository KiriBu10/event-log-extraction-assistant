'''
    Metrics calculations relaxed by mdees.
'''
import pandas as pd

def dataframe_similarity(df1, df2):
    # Ensure both dataframes compare the same columns, sorted alphabetically
    if set(df1.columns) != set(df2.columns):
        return "Can't calculate Precision, Recall and F1. DataFrames must have the same columns"

    df1 = df1.sort_values(by=list(df1.columns)).reset_index(drop=True)
    df2 = df2.sort_values(by=list(df1.columns)).reset_index(drop=True)
    # print('groundtruth\n',df1.head())
    # print('generated\n',df2.head())
    # print('groundtruth',df1.shape)
    # print('generated',df2.shape)


    # Comparison based on all columns

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


    # Comparison based on all columns except activity_id

    # drop columns with activity_id
    df1=df1.drop(['activity_id','combined'], axis=1)
    df2=df2.drop(['activity_id','combined'], axis=1)

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
    relaxed_precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    relaxed_recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    relaxed_f1 = 2 * (relaxed_precision * relaxed_recall) / (relaxed_precision + relaxed_recall) if (relaxed_precision + relaxed_recall) > 0 else 0

    return {'precision':round(precision,3), 'recall':round(recall,3), 'f1':round(f1,3),'relaxed_precision':round(relaxed_precision,3), 'relaxed_recall':round(relaxed_recall,3), 'relaxed_f1':round(relaxed_f1,3)}
