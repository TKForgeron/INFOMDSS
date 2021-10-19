import pandas as pd
from datetime import datetime

def get_vaccinations_df_il(df: pd.DataFrame, months: int = None) -> pd.DataFrame:


    """

    Function that sums list of vaccination columns, aggregates on town code and creates incremental vaccination count based on cummulative data
    Returns: sorted pd.DataFrame with the total vaccinations in Israel per date

    """

    df.columns = [x.lower() for x in df.columns]
    age_groups = ['0-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90+']
    vaccination_columns = [[f'first_dose_{age_group}', f'second_dose_{age_group}',f'third_dose_{age_group}'] for age_group in age_groups]
    vaccination_columns = [item for sublist in vaccination_columns for item in sublist]

    df[vaccination_columns] = df[vaccination_columns].replace(to_replace="<15", value="0").astype(float)
    df['accumulated_vaccinations'] = df[vaccination_columns].sum(axis=1)

    df["vaccinations"] = df.groupby(["citycode"])["accumulated_vaccinations"].transform(
        lambda s: s.sub(s.shift().fillna(0)).abs()
    )
    df = df.groupby("date")["vaccinations"].sum().reset_index()
    df["date"] = pd.to_datetime(df["date"])
    
    if months:
        df = df[df["date"] > datetime.now() - pd.DateOffset(months=months)]

    df = df.sort_values(by=["date"])

    df.to_csv('output.csv',index=False)
    return df


def get_vaccinations_df_nl(df: pd.DataFrame) -> pd.DataFrame:
    pass


def get_vaccinations_df_nsw(df: pd.DataFrame) -> pd.DataFrame:
    pass
