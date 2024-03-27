import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin
from typing import List, Union, Optional
from ast import literal_eval


class LogAfterZeroReplacement(BaseEstimator, TransformerMixin):
    """
    Takes a numerical column and replaces any zero values before
    taking the natural logarithm.

    Parameters:
        cols: Names of columns to transform.
        zero_replacement: Value to replace zero with.
    """

    def __init__(
        self,
        cols: str,
        zero_replacement: float,
    ):
        self.cols = cols
        self.zero_replacement = zero_replacement

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X, y=None) -> pd.DataFrame:
        """Replaces zero before applying natural log."""

        # TODO: check for clash in column names?
        # TODO: raise warning if column not int/float type

        # Check for negative values
        cols_with_neg_values = [col for col in self.cols if (X[col] < 0).sum() > 0]
        assert cols_with_neg_values == [], (
            "Found columns with negative values:",
            cols_with_neg_values,
            "Replace before transforming.",
        )

        if self.zero_replacement == 1:
            for col in self.cols:
                X[f"{col}__log"] = X[col].apply(np.log1p)

        else:
            X[f"{col}__log"] = X[col].replace(0, self.zero_replacement).apply(np.log)

        return X


class FlagIfStrContains(BaseEstimator, TransformerMixin):
    """
    Takes a string column and creates a dummy column that indicates
    whether the string contains any of the provided tokens. The
    matching is currently not case sensitive.

    Parameters:
        cols: Names of column to transform.
        new_col: Name to give indicator column.
        tokens_to_match: Tokens to perform matching on.
    """

    def __init__(
        self,
        col: str,
        new_col: str,
        tokens_to_match: List[str],
    ):
        # TODO: add optional case matching
        self.col = col
        self.new_col = new_col
        self.tokens_to_match = [token.lower() for token in tokens_to_match]

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X, y=None) -> pd.DataFrame:
        """Creates binary indicator if matching string found."""

        # TODO: check for clash in column names?
        # TODO: raise warning if column not object type

        X[self.new_col] = (
            X[self.col].str.lower().apply(lambda x: any(p for p in self.tokens_to_match if p in x.split(" ")))
        )

        return X


class OneHotEncodeFromTags(BaseEstimator, TransformerMixin):
    """
    Takes a column of tags and one-hot encodes them to create a
    set of dummy variables (one per tag).

    Parameters:
        cols: Names of columns to transform.
        order_by: How should the tags be ordered before the columns
            are created?
    """

    def __init__(self, cols: List[str], order_by: Optional[Union["popularity", "alphabet", None]] = None):
        if isinstance(cols, str):
            self.cols = [cols]
        else:
            self.cols = cols
        self.unique_tags = {col: [] for col in cols}
        self.order_by = order_by

    def get_unique_tags(self, x: Union[np.array, pd.Series]) -> List:
        """Gets a list of unique values across an array of lists"""

        all_tags = [literal_eval(sublist) for sublist in np.unique(x)]
        flattened_tags = [tag for tag_list in all_tags for tag in tag_list]

        unique_tags = list(set(flattened_tags))

        # Sort from most to least popular
        if self.order_by == "popularity":
            unique_tags = [
                tag for _, tag in sorted(zip([flattened_tags.count(tag) for tag in unique_tags], unique_tags))
            ]

        elif self.order_by == "alphabet":
            unique_tags = sorted(unique_tags)

        return unique_tags

    def fit(self, X: pd.DataFrame, y=None):
        """Gets unique tags in each column and applies one-hot encoding."""

        # TODO: avoid double for-loop
        for col in self.cols:
            # Get list of tags
            self.unique_tags[col] = self.get_unique_tags(X[col])

            # One-hot encode each tag
            for tag in self.unique_tags[col]:
                X[f"{col}__{tag}"] = X[col].apply(lambda x: 1 if tag in x else 0)

        return self

    def transform(self, X, y=None) -> pd.DataFrame:
        """Applies one-hot encoding based on existing tags"""

        # TODO: check for clashes in column names?
        # TODO: avoid double for-loop

        new_tags = {col: None for col in self.cols}

        for col in self.cols:
            # Get list of tags
            new_tags[col] = self.get_unique_tags(X[col])

            if any(tag for tag in new_tags if tag not in self.unique_tags[col]):
                # TODO: raise warning if new tags encountered
                pass

            for tag in self.unique_tags[col]:
                X[f"{col}__{tag}"] = X[col].apply(lambda x: 1 if tag in x else 0)

        return X


class ColumnDropper(BaseEstimator, TransformerMixin):
    """
    Drops columns from a Pandas DF.

    Parameters:
        cols: Names of columns to drop
    """

    def __init__(self, cols: List[str]):
        self.cols = cols

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None) -> pd.DataFrame:
        return X.drop(self.cols, axis=1)
