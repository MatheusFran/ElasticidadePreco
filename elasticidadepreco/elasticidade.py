

def elasticidade(df,var1,var2):
    df['change_qtd'] = df[var1].pct_change()
    df['change_price'] = df[var2].pct_change()
    df['elasticity'] = df['change_qtd']/df['change_price']
    return df