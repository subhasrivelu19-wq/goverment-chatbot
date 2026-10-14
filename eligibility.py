import pandas as pd

def filter_by_profile(df: pd.DataFrame, age: int, state: str, occupation: str, income: str) -> pd.DataFrame:
    # Transparent keyword matching for a classroom demo; not a legal eligibility checker.
    data = df.copy()
    if state == "Tamil Nadu":
        data = data[data["government_level"].isin(["Central", "Tamil Nadu"])]
    if occupation == "Student":
        mask = data[["category", "target_group", "scheme_name"]].astype(str).apply(
            lambda col: col.str.contains("education|student|school|college|scholarship|girl|youth|skill", case=False, regex=True)
        ).any(axis=1)
        data = data[mask]
    elif occupation == "Farmer":
        mask = data[["category", "target_group", "scheme_name"]].astype(str).apply(
            lambda col: col.str.contains("agriculture|farmer|kisan|fisher|fisheries|livestock", case=False, regex=True)
        ).any(axis=1)
        data = data[mask]
    elif occupation == "Women":
        mask = data[["category", "target_group", "scheme_name"]].astype(str).apply(
            lambda col: col.str.contains("women|girl|maternity|woman", case=False, regex=True)
        ).any(axis=1)
        data = data[mask]
    elif occupation == "Worker":
        mask = data[["category", "target_group", "scheme_name"]].astype(str).apply(
            lambda col: col.str.contains("worker|employment|labour|pension|skill", case=False, regex=True)
        ).any(axis=1)
        data = data[mask]
    elif occupation == "Business owner":
        mask = data[["category", "target_group", "scheme_name"]].astype(str).apply(
            lambda col: col.str.contains("business|entrepreneur|credit|msme|enterprise", case=False, regex=True)
        ).any(axis=1)
        data = data[mask]
    elif occupation == "Senior citizen":
        mask = data[["category", "target_group", "scheme_name"]].astype(str).apply(
            lambda col: col.str.contains("senior|old age|pension|social security", case=False, regex=True)
        ).any(axis=1)
        data = data[mask]
    elif occupation == "Person with disability":
        mask = data[["category", "target_group", "scheme_name"]].astype(str).apply(
            lambda col: col.str.contains("disability|disabled|disabilities|assistive", case=False, regex=True)
        ).any(axis=1)
        data = data[mask]
    elif occupation == "Fisher":
        mask = data[["category", "target_group", "scheme_name"]].astype(str).apply(
            lambda col: col.str.contains("fisher|fisheries|fishers", case=False, regex=True)
        ).any(axis=1)
        data = data[mask]
    return data
