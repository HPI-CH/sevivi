from typing import List, Optional, Dict, Union

import pandas as pd


def get_graph_groups(
    df: pd.DataFrame, patterns: Optional[List[str]]
) -> Dict[str, List[str]]:
    if patterns is None:
        return {col: [col] for col in df.columns}
    else:
        return {pattern: find_matching_columns(df, pattern) for pattern in patterns}


def find_matching_columns(
    df: pd.DataFrame, pattern: Union[str, List[str]]
) -> List[str]:
    if isinstance(pattern, str):
        return [col for col in df.columns if pattern in col]
    else:
        column_set = set(df.columns)
        desired_column_set = set(pattern)
        if len(desired_column_set - column_set) > 0:
            raise ValueError(f"Unknown columns {desired_column_set - column_set}")
        return pattern
