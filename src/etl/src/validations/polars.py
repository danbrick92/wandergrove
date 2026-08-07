import polars as pl
from exceptions.schema_validation_exception import SchemaValidationException


def validate_no_blank_strings(df: pl.DataFrame, column_name: str) -> None:
    df_blank = df.filter(pl.col(column_name).is_null() | (pl.col(column_name) == ""))
    if df_blank.shape[0] > 0:
        raise SchemaValidationException("location contains blank location(s)")
