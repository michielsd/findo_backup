import pandas as pd

JAAR_MIN = 2017
JAAR_MAX = 2025

FOLDER_PATH = "C:/Dashboard/Werk/Iv3data/"
# Begroting en jaarrekening handmatig

def pivotIv3(df, jaar):
    print("[INFO] Pivoting for year ", jaar)
    df = df.dropna(subset=["k_2ePlaatsing_2"])
    
    pv = df.pivot(
        index=["Gemeenten", "TaakveldBalanspost"],
        columns="Categorie",
        values=["k_2ePlaatsing_2"]
    )
    
    pv.columns = [col[-1] for col in pv.columns]
    
    batencolumns = [col for col in pv.columns if col.startswith("B")]
    lastencolumns = [col for col in pv.columns if col.startswith("L")]

    pv['Baten'] = pv[batencolumns].sum(axis=1)
    pv['Lasten'] = pv[lastencolumns].sum(axis=1)
    pv['Saldo'] = pv.apply(lambda row: row.Baten - row.Lasten, axis=1)
    
    pv = pv.reset_index()
    pv.insert(1, "Jaar", jaar)
    
    # Taakvelddata
    df_alleen_bl = pv.drop(columns=["Primo", "Ultimo"])
    df_bl = df_alleen_bl.melt(
        id_vars=["Gemeenten", "Jaar", "TaakveldBalanspost"],
        var_name="Categorie",
        value_name="k_2ePlaatsing_2"
    )
    df_bl = df_bl.loc[~df_bl["TaakveldBalanspost"].str.startswith(("A", "P"))]
    df_bl = df_bl.dropna(subset=["k_2ePlaatsing_2"])
    df_bl = df_bl.rename(columns={
        "TaakveldBalanspost": "Taakveld", 
        "k_2ePlaatsing_2": "Waarde"
    })
    for col in df_bl.columns:
        if col != "Waarde":
            df_bl[col] = df_bl[col].astype(str)

    # Balanspostdata
    df_bp = pv[["Gemeenten", "Jaar", "TaakveldBalanspost", "Ultimo"]]
    df_bp = df_bp.dropna(subset=["Ultimo"])
    df_bp = df_bp.rename(columns={
        "TaakveldBalanspost": "Balanspost", 
        "Ultimo": "Waarde"
    })
    for col in df_bp.columns:
        if col != "Waarde":
            df_bp[col] = df_bp[col].astype(str)
    
    print("[INFO] Pivoting for year ", jaar, " done")

    return df_bl, df_bp


# Main processing
bl_list = []
bp_list = []

for jaar in range(JAAR_MIN, JAAR_MAX + 1):
    df = pd.read_csv(f"{FOLDER_PATH}{jaar}000.csv")
    batenlasten, balansposten = pivotIv3(df, jaar)
    bl_list.append(batenlasten)
    bp_list.append(balansposten)

batenlasten = pd.concat(bl_list)
balansposten = pd.concat(bp_list)

# Save results
batenlasten.to_pickle("begroting_batenlasten.pickle")
balansposten.to_pickle("rekening_balansposten.pickle")

print("Done!")