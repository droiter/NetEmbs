# encoding: utf-8
__author__ = 'Aleksei Maliutin'
"""
evaluation.py
Created by lex at 2019-07-08.
"""
import pandas as pd
from typing import Optional, Dict
from sklearn.metrics import v_measure_score, adjusted_mutual_info_score, adjusted_rand_score, fowlkes_mallows_score


def overall_score(df, column_true="GroundTruth", column_pred="label"):
    return list(evaluate_all(df, column_true=column_true, column_pred=column_pred).values())


def evaluate_all(df: pd.DataFrame, column_true: str = "GroundTruth", column_pred: str = "label", postfix: str = "",
                 full_names: Optional[bool] = False) -> Dict[str, float]:
    """
    Evaluate all available metrics for the given predicted and true labels.

    Parameters
    ----------
    df : DataFrame
        Input DataFrame with at least two columns: True and Predicted ones
    column_true : str, default if 'GroundTruth'
        The title for column with True labels
    column_pred : str, default is 'label'
        The title for column with Predicted labels
    postfix : str, default is ''
        Postfix to be add to the metric names
    full_names : bool, default if False
        Use full metrics name.

    Returns
    -------
    Dictionary: Metric->Score
    """
    output_result = dict()
    str_labels = list(df[column_true].unique())
    real_labels = dict(zip(str_labels, range(len(str_labels))))
    true_values = df[column_true].apply(lambda x: real_labels[x]).values
    predicted_values = df[column_pred].values
    if full_names:
        #     ARI
        output_result["Adjusted Rand index" + postfix] = adjusted_rand_score(true_values, predicted_values)
        #     AMI
        output_result["Adjusted Mutual Information" + postfix] = adjusted_mutual_info_score(true_values,
                                                                                            predicted_values,
                                                                                            average_method="arithmetic")
        #     V-Score
        output_result["V-measure" + postfix] = v_measure_score(true_values, predicted_values)
        #     The Fowlkes-Mallows index
        output_result["Fowlkes-Mallows index" + postfix] = fowlkes_mallows_score(true_values, predicted_values)
    else:
        #     ARI
        output_result["ARI" + postfix] = adjusted_rand_score(true_values, predicted_values)
        #     AMI
        output_result["AMI" + postfix] = adjusted_mutual_info_score(true_values,
                                                                    predicted_values,
                                                                    average_method="arithmetic")
        #     V-Score
        output_result["V-M" + postfix] = v_measure_score(true_values, predicted_values)
        #     The Fowlkes-Mallows index
        output_result["FMI" + postfix] = fowlkes_mallows_score(true_values, predicted_values)
    return output_result


def v_measure(df: pd.DataFrame, column_true: str = "GroundTruth", column_pred: str = "label") -> float:
    """
    V-measure cluster labeling given a ground truth.

    This metric is independent of the absolute values of the labels:
    a permutation of the class or cluster label values won’t change the score value in any way.
    Parameters
    ----------
    df : DataFrame
        Input DataFrame with at least two columns: True and Predicted ones
    column_true : str, default if 'GroundTruth'
        The title for column with True labels
    column_pred : str, default is 'label'
        The title for column with Predicted labels

    Returns
    -------
    V-Measure score
    """
    str_labels = list(df[column_true].unique())
    real_labels = dict(zip(str_labels, range(len(str_labels))))
    return v_measure_score(df[column_true].apply(lambda x: real_labels[x]).values, df[column_pred].values)


def fowlkes_mallows_index(df: pd.DataFrame, column_true: str = "GroundTruth", column_pred: str = "label") -> float:
    """
    Measure the similarity of two clusterings of a set of points.

    The Fowlkes-Mallows index (FMI) is defined as the geometric mean between of the precision and recall:
                            FMI = TP / sqrt((TP + FP) * (TP + FN))
    TThe score ranges from 0 to 1. A high value indicates a good similarity between two clusters.
    Parameters
    ----------
    df : DataFrame
        Input DataFrame with at least two columns: True and Predicted ones
    column_true : str, default if 'GroundTruth'
        The title for column with True labels
    column_pred : str, default is 'label'
        The title for column with Predicted labels

    Returns
    -------
    The FMI returns a value of from 0.0 to 1.0: Perfect labeling is scored 1.0,
    while Bad (e.g. independent labelings) have zero scores:
    """
    str_labels = list(df[column_true].unique())
    real_labels = dict(zip(str_labels, range(len(str_labels))))
    return fowlkes_mallows_score(df[column_true].apply(lambda x: real_labels[x]).values, df[column_pred].values)


def adjusted_mutual_info(df: pd.DataFrame, column_true: str = "GroundTruth", column_pred: str = "label") -> float:
    """
    Adjusted Mutual Information between two clusterings.

    This metric is independent of the absolute values of the labels: a permutation of the class
    or cluster label values won’t change the score value in any way.
    Parameters
    ----------
    df : DataFrame
        Input DataFrame with at least two columns: True and Predicted ones
    column_true : str, default if 'GroundTruth'
        The title for column with True labels
    column_pred : str, default is 'label'
        The title for column with Predicted labels

    Returns
    -------
    The AMI returns a value of 1 when the two partitions are identical (ie perfectly matched).
    Random partitions (independent labellings) have an expected AMI around 0 on average hence can be negative.
    """
    str_labels = list(df[column_true].unique())
    real_labels = dict(zip(str_labels, range(len(str_labels))))
    return adjusted_mutual_info_score(df[column_true].apply(lambda x: real_labels[x]).values, df[column_pred].values,
                                      average_method="arithmetic")


def adjusted_rand_index(df: pd.DataFrame, column_true: str = "GroundTruth", column_pred: str = "label") -> float:
    """
    Rand index adjusted for chance.


    The Rand Index computes a similarity measure between two clusterings by considering all pairs of samples
        and counting pairs that are assigned in the same or different clusters in the predicted and true clusterings.
    The adjusted Rand index is thus ensured to have a value close to 0.0 for random labeling independently of the number of clusters
        and samples and exactly 1.0 when the clusterings are identical (up to a permutation).
    Parameters
    ----------
    df : DataFrame
        Input DataFrame with at least two columns: True and Predicted ones
    column_true : str, default if 'GroundTruth'
        The title for column with True labels
    column_pred : str, default is 'label'
        The title for column with Predicted labels

    Returns
    -------
    Similarity score between -1.0 and 1.0.
    Random labellings have an ARI close to 0.0. 1.0 stands for perfect match
    """
    str_labels = list(df[column_true].unique())
    real_labels = dict(zip(str_labels, range(len(str_labels))))
    return adjusted_rand_score(df[column_true].apply(lambda x: real_labels[x]).values, df[column_pred].values)
