import pandas as pd


def infos(df: pd.DataFrame, include_head: bool = False, sort_by_dtype: bool = True):
    """
    Merges together df.info and df.describe commonly used in EDA
    Also adds columns :
    - count of nulls (vs df.info "Non-Null Count")
    - nulls percentage (convenience)
    - number of unique values (useful to spot low cardinality;
         conversion to catogorical data type candidates)
    """
    print("shape       :", df.shape)
    print(
        "dtypes      :",
        [
            (f"{dt}({ct})")
            for dt, ct in zip(
                df.dtypes.value_counts().index.to_list(),
                df.dtypes.value_counts().to_list(),
            )
        ],
    )
    if (df.dtypes == "object").any() or (df.dtypes == "str").any():
        bytes = df.memory_usage(deep=True).sum()
        for unit, threshold in [
            ("TB", 1024**4),
            ("GB", 1024**3),
            ("MB", 1024**2),
            ("KB", 1024),
        ]:
            if bytes >= threshold:
                print(f"memory usage: {bytes / threshold:.2f} {unit}")
                break
        else:
            print(f"memory usage: {bytes} bytes")

    if include_head:
        display(df.head(10))

    def _dtype_sort_key(dtype):
        s = str(dtype)
        sl = s.lower()
        if s == "category":
            return 0
        if s == "object":
            return 1
        if s in ("str", "string"):
            return 2
        if s in ("bool", "boolean"):
            return 3
        # interval must be checked before int (its str repr starts with "int")
        if sl.startswith("interval"):
            return 10
        if sl.startswith("int") or sl.startswith("uint"):   # int8…int64, Int8…UInt64
            return 4
        if sl.startswith("float") or sl.startswith("sparse"):  # float16…Float64, Sparse[float…]
            return 5
        if sl.startswith("complex"):
            return 6
        if sl.startswith("datetime"):
            return 7
        if sl.startswith("timedelta"):
            return 8
        if sl.startswith("period"):
            return 9
        return 11

    result = pd.concat(
        [
            df.isna().sum().rename("nulls"),
            (df.isna().sum() / df.shape[0]).rename("nulls_pct").round(3) * 100,
            df.dtypes.rename("dtypes"),
            df.nunique().rename("nunique"),
        ],
        axis="columns",
    ).merge(
        df.select_dtypes(exclude="complex").describe().T.round(3),
        how="left",
        left_index=True,
        right_index=True,
    )

    if not sort_by_dtype:
        return result

    result["_sort"] = result["dtypes"].map(_dtype_sort_key)
    return result.sort_values("_sort").drop(columns="_sort")


def test_infos_dtype_ordering():
    # In pandas 3.x: string-like object columns → "str" dtype; mixed-type columns → "object" dtype
    df = pd.DataFrame(
        {
            # out-of-order on purpose
            "interval_col": pd.arrays.IntervalArray([pd.Interval(0, 1), pd.Interval(1, 2), pd.Interval(2, 3)]),
            "Float64_col":  pd.array([1.1, 2.2, None], dtype="Float64"),  # nullable float
            "float64_col":  pd.array([1.1, 2.2, None], dtype="float64"),
            "period_col":   pd.period_range("2021", periods=3, freq="D"),
            "Int64_col":    pd.array([1, 2, None], dtype="Int64"),         # nullable int
            "int32_col":    pd.array([1, 2, 3], dtype="int32"),
            "datetime_col": pd.array(["2021-01-01", "2021-01-02", "2021-01-03"], dtype="datetime64[ns]"),
            "timedelta_col": pd.array([pd.Timedelta("1D"), pd.Timedelta("2D"), pd.Timedelta("3D")]),
            "bool_col":     pd.array([True, False, True], dtype="bool"),
            "boolean_col":  pd.array([True, False, None], dtype="boolean"),
            "complex_col":  pd.array([1+2j, 3+4j, 5+6j], dtype="complex128"),
            "o_col":        pd.array([1, "two", None], dtype="object"),    # true mixed object
            "s_col":        pd.array(["x", "y", "z"], dtype="string"),     # pd.StringDtype → "string"
            "str_col":      pd.array(["a", "b", None], dtype="object"),    # string-like → "str" in pandas 3.x
            "c_col":        pd.Categorical(["p", "q", "p"]),
        }
    )
    result = infos(df)
    expected_order = [
        "c_col",                          # 0  category
        "o_col",                          # 1  object
        "s_col", "str_col",               # 2  string / str
        "bool_col", "boolean_col",        # 3  bool
        "Int64_col", "int32_col",         # 4  int (nullable + numpy)
        "Float64_col", "float64_col",     # 5  float (nullable + numpy)
        "complex_col",                    # 6  complex
        "datetime_col",                   # 7  datetime
        "timedelta_col",                  # 8  timedelta
        "period_col",                     # 9  period
        "interval_col",                   # 10 interval
    ]
    assert list(result.index) == expected_order, (
        f"Expected:\n  {expected_order}\nGot:\n  {list(result.index)}\n"
        f"Dtypes: {[(c, str(result.loc[c, 'dtypes'])) for c in result.index]}"
    )

    # Columns added out-of-order should still sort correctly
    df2 = pd.DataFrame(
        {
            "z_Float64": pd.array([1.0, 2.0], dtype="Float64"),
            "a_Int64":   pd.array([1, 2], dtype="Int64"),
            "b_float64": pd.array([1.0, 2.0], dtype="float64"),
            "c_int32":   pd.array([1, 2], dtype="int32"),
            "m_cat":     pd.Categorical(["x", "y"]),
        }
    )
    result2 = infos(df2)
    assert list(result2.index) == ["m_cat", "a_Int64", "c_int32", "z_Float64", "b_float64"], (
        f"Unexpected order: {list(result2.index)}"
    )

    # sort_by_dtype=False preserves original column order
    df3 = pd.DataFrame(
        {
            "z_float": pd.array([1.0, 2.0], dtype="float64"),
            "a_int":   pd.array([1, 2], dtype="int64"),
            "m_cat":   pd.Categorical(["x", "y"]),
        }
    )
    result3 = infos(df3, sort_by_dtype=False)
    assert list(result3.index) == ["z_float", "a_int", "m_cat"], (
        f"sort_by_dtype=False should preserve input order, got {list(result3.index)}"
    )

    print("test_infos_dtype_ordering passed")


def summary_value_counts(s: pd.Series | pd.api.typing.SeriesGroupBy):
    """Combines `value_counts()` and `values_counts(normalize=True)``
    If the series has a name, the count column is renmed to preserve chaining via dot notation
    (otherwise .count is a series or dataframe method)
    """
    col_count = s.value_counts()
    col_pct = s.value_counts(normalize=True).mul(100).round(1)

    if isinstance(s, pd.api.typing.SeriesGroupBy) or not s.name:
        return pd.DataFrame({f"value_count": col_count, "pct": col_pct})
    else:
        return pd.DataFrame({f"{s.name}_count": col_count, "pct": col_pct})
