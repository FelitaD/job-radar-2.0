import streamlit as st
import pandas as pd
import re

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)


def filter_dataframe(df: pd.DataFrame, key=None) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe
        key: the unique identifier for the checkbox

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters", key=key)

    if not modify:
        return df

    modification_container = st.container()
    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)

    for column in to_filter_columns:
        left, right = st.columns((1, 20))
        left.write("↳")

        if is_numeric_dtype(df[column]):
            _min = float(df[column].min())
            _max = float(df[column].max())
            step = 0.1

        if is_categorical_dtype(df[column]) or df[column].nunique() < 80:
            user_cat_input = right.multiselect(
                f"Values for {column}",
                df[column].unique(),
                default=list(df[column].unique()),
            )
            df = df[df[column].isin(user_cat_input)]

        elif is_numeric_dtype(df[column]):
            _min = float(df[column].min())
            _max = float(df[column].max())
            step = (_max - _min) / 100

            user_num_input = right.slider(
                f"Values for {column}",
                min_value=_min,
                max_value=_max,
                value=(_min, _max),
                step=step,
            )
            df = df[df[column].between(*user_num_input)]

        elif df[column].name == 'title':
            user_text_input = right.text_input(
                f"Substring or regex in {column}",
            )
            if user_text_input:
                df = df[df[column].astype(str).str.contains(user_text_input,  regex=True, na=False)]

        elif df[column].name == 'company':
            user_cat_input = right.multiselect(
                f"Values for {column}",
                df[column].sort_values().unique(),
            )
            df = df[df[column].isin(user_cat_input)]

        elif df[column].name == 'stack':
            user_cat_input = right.multiselect(
                f"Values for {column}",
                df[column].sort_values().unique(),
            )
            df = df[df[column].isin(user_cat_input)]

        # elif is_datetime64_any_dtype(df[column]):
        #     user_date_input = right.date_input(
        #         f"Values for {column}",
        #         value=(
        #             df[column].min(),
        #             df[column].max(),
        #         ),
        #     )
        #     if len(user_date_input) == 2:
        #         user_date_input = tuple(map(pd.to_datetime, user_date_input))
        #         start_date, end_date = user_date_input
        #         df = df.loc[df[column].between(start_date, end_date)]
        #
        #     else:
        #         user_text_input = right.text_input(
        #             f"Substring or regex in {column}",
        #         )
        #         if user_text_input:
        #             df = df[df[column].astype(str).str.contains(user_text_input)]

        elif is_datetime64_any_dtype(df[column]):
            user_date_input = right.date_input(
                f"Values for {column}",
                value=(
                    df[column].min(),
                    df[column].max(),
                ),
            )
            if len(user_date_input) == 2:
                user_date_input = tuple(map(pd.to_datetime, user_date_input))
                start_date, end_date = user_date_input
                df = df.loc[df[column].between(start_date, end_date)]

            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

        return df