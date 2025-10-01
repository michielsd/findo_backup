import pandas as pd

KENGETALLEN_FILE = "C:/Dashboard/Werk/kengetallen_eindversie_2.xlsx"

xls = pd.read_excel(KENGETALLEN_FILE, sheet_name=None)

# Get sheets
sheets = [s for s in xls.keys() if s.startswith("20")]

def main():
    dfs = []
    
    for sheet in sheets:
        dfs.append(process_sheet(sheet))
    
    df = pd.concat(dfs)
    df.to_pickle("kengetallen.pickle")

def process_sheet(sheet):
    df = xls[sheet]
    df = df.fillna("")
    
    # Collect kengetallen and jaar
    kengetallen = []
    jaren = []
    type_ramingen = []
    
    kengetal = ""
    for k, j in zip(df.iloc[0,:], df.iloc[1,:]):
        if k != "":
            kengetal = k
            kengetallen.append(kengetal)
        else:    
            kengetallen.append(kengetal)
        jaren.append(j[:4])
        type_ramingen.append(j[5:])
    
    # Collect values
    rows = []
    for r in range(2, len(df)):
        gemeentecode = df.iloc[r, 0]
        gemeentenaam = df.iloc[r, 1]
        
        for c in range(2, len(df.columns)):
            kengetal = kengetallen[c]
            jaar = jaren[c]
            type_raming = type_ramingen[c]
            waarde = df.iloc[r, c]
            rows.append([gemeentenaam, sheet, kengetal, jaar, type_raming, waarde])
    
    df = pd.DataFrame(rows, columns=["Gemeenten", "Begroting", "Kengetal", "Jaar", "Type raming", "Waarde"])
    
    return df

if __name__ == "__main__":
    main()