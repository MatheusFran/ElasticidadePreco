import pandas as pd

def outliersCalc(df):
    outliers = pd.DataFrame(False, index=df.index, columns=df.columns)
    for col in df.columns:
        lower = df[col].mean() - 3 * df[col].std()
        upper = df[col].mean() + 3 * df[col].std()
        outliers[col] = ~df[col].between(lower, upper)
    return outliers
