import pandas as pd


def outliersCalc(df):
    outliers = pd.DataFrame(False, index=df.index, columns=df.columns)
    for col in df.columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers[col] = ~df[col].between(lower, upper)
    return outliers
