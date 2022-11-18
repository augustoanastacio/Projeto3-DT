import pandas as pd


# FUNÇÃO FEITA PELA YANA QUE É UTILIZADA EM UMA DAS FUNÇÕES
def df_to_analysis(all_jsons: list, column_name: str):
    new_json = {}
    n = 0
    for week in range(len(all_jsons)):
        for transaction in range(len(all_jsons[week])):
            balance = 0
            new_json[n] = {}
            new_json[n]['date'] = all_jsons[week][transaction]['date']
            new_json[n]['week'] = f'Week {week+1}'
            new_json[n]['month']=all_jsons[week][transaction]['date']
            new_json[n]['id'] = all_jsons[week][transaction]['id']
            for i in range(0,21):
                new_json[n][f'prod_{i}'] = 0
            for key in all_jsons[week][transaction]:
                if ('prod' in key):
                    if (type(all_jsons[week][transaction][key][column_name])==list): #teste
                        new_json[n][key] = float(all_jsons[week][transaction][key][column_name][0])
                    else:
                        new_json[n][key] = float(all_jsons[week][transaction][key][column_name])
                    balance += new_json[n][key]
            n += 1
    df = pd.DataFrame(new_json).T
    df['balance'] = balance
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['month'] = pd.to_datetime(df['month']).dt.month_name()
    return df


def plot_prod_qnt(all_df):
    group_qnt = all_df.groupby('product')['qnt'].sum()
    df_prod = pd.DataFrame(group_qnt)
    plot_prod = df_prod.plot(kind='bar')
    return plot_prod


def plot_month_balance(all_df):
    df_balance = all_df.copy()
    df_balance['balance'] = df_balance['qnt'] * df_balance['price']
    df_months_balance = pd.DataFrame(df_balance.groupby('month')['balance'].sum())
    plot_months = df_months_balance.plot(kind='pie', subplots=True)
    return plot_months


def all_sales_csv(all_jsons):
    all_qnt = df_to_analysis(all_jsons=all_jsons, column_name='qnt')
    all_qnt.to_csv('all_sales.csv', index=False)
