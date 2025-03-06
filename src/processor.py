import pandas as pd
import io


def load_file(f):
    try:
        df = pd.read_csv(f)
    except:
        df = pd.read_excel(f)
    return df


def create_download_link(data):
    """Generates an Excel file for download from a dictionary of DataFrames."""
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        for sheet_name, df in data.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        writer.close()

    buffer.seek(0)  # Reset buffer position
    return buffer


def generate_report(df_gross: pd.DataFrame, df_leads_pipeline: pd.DataFrame) -> pd.DataFrame:
    # Rename columns
    df_gross.columns = ["id", "created_on", "email", "name", "phone", "state"]
    df_leads_pipeline.columns = ["id", "submit_date", "name", "email", "phone", "source"]

    # Merge data
    result = (df_gross
        .drop(columns=["id"])
        .loc[
            (df_gross["state"] == "Excluded") 
            & (df_gross["email"].notnull())
            & (df_gross["phone"].notnull())
            & ~(df_gross["phone"].isin(df_leads_pipeline["phone"]))
        ]
        .drop_duplicates(subset=["email", "phone"])
        .reset_index(drop=True)
    )
    return result

def generate_download_dict(df: pd.DataFrame) -> dict:
    return {"Gross Leads not in Leads & Pipe": df}