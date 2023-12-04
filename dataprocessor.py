import pandas as pd


def process_data(csv):
    # Namen der Spalten festlegen
    column_names = ['HSN',
                    'Fahrzeughersteller',
                    'TSN',
                    'Fahrzeugklasse',
                    'Handelsname',
                    'Kraftstoffcode',
                    'Leistung',
                    'Emissionscode',
                    'Co2_kombiniert',
                    'Co2_gewichtet',
                    'Co2_kombiniert2',
                    'Co2_gewichtet2',
                    'Verbrauch_kombiniert',
                    'Verbrauch_gewichtet',
                    'Verbrauch_kombiniert2',
                    'Verbrauch_gewichtet2',
                    ]
    # Datentypen festlegen
    data_types = {'HSN': 'object',
                  'Fahrzeughersteller': 'object',
                  'TSN': 'object',
                  'Fahrzeugklasse': 'object',
                  'Handelsname': 'object',
                  'Kraftstoffcode': 'object',
                  'Leistung': 'float64',
                  'Emissionscode': 'object',
                  'Co2_kombiniert': 'float64',
                  'Co2_gewichtet': 'float64',
                  'Co2_kombiniert2': 'float64',
                  'Co2_gewichtet2': 'float64',
                  'Verbrauch_kombiniert': 'float64',
                  'Verbrauch_gewichtet': 'float64',
                  'Verbrauch_kombiniert2': 'float64',
                  'Verbrauch_gewichtet2': 'float64',
                  }
    # beide übergebenen csv in dataframes laden
    pkw_df = pd.read_csv(csv[0], names=column_names, dtype=data_types)
    lkw_df = pd.read_csv(csv[1], names=column_names, dtype=data_types)

    pkw_df['Fahrzeugtyp'] = 'PKW'
    lkw_df['Fahrzeugtyp'] = 'LKW'

    # beide dataframes zusammenführen
    df = pd.concat([pkw_df, lkw_df])

    # überflüssige leere Reihen löschen
    df = df[(df['TSN'] != "2") & (~df['TSN'].isnull())]

    # Entfernen der Nachkommastellen (.0) in beiden columns,in denen Zahlen als String mit führenden nullen stehen sollen
    # mithilfe regular expressions
    df['HSN'] = df['HSN'].str.replace(r'\.0$', '', regex=True)
    df['Kraftstoffcode'] = df['Kraftstoffcode'].str.replace(r'\.0$', '', regex=True)

    # Auffüllen der Stringspalten mit Zahlen mit führenden Nullen bis zur Länge 4
    df['HSN'] = df['HSN'].str.zfill(4)
    df['Kraftstoffcode'] = df['Kraftstoffcode'].str.zfill(4)

    # Auffüllen der NaN-Werte mit datenttyp-gemäßen Füllwerten
    df['Verbrauch_gewichtet'] = df['Verbrauch_gewichtet'].fillna(0)
    df['Verbrauch_gewichtet2'] = df['Verbrauch_gewichtet2'].fillna(0)
    df['Verbrauch_kombiniert'] = df['Verbrauch_kombiniert'].fillna(0)
    df['Verbrauch_kombiniert2'] = df['Verbrauch_kombiniert2'].fillna(0)
    df['Co2_kombiniert'] = df['Co2_kombiniert'].fillna(0)
    df['Co2_gewichtet'] = df['Co2_gewichtet'].fillna(0)
    df['Co2_kombiniert2'] = df['Co2_kombiniert2'].fillna(0)
    df['Co2_gewichtet2'] = df['Co2_gewichtet2'].fillna(0)

    df['Emissionscode'] = df['Emissionscode'].fillna("-")
    df['Handelsname'] = df['Handelsname'].fillna("-")

    # Gruppieren nach HSN und TSN und die Indexe der jeweils größten CO2_kombiniert_Werte suchen
    idx_to_keep = df.groupby(['TSN', 'HSN'])['Co2_kombiniert'].idxmax()

    # Nur die Zeilen behalten, die den ausgewählten Indexen entsprechen um nur einen (den höchsten) Wert für Co2_kombiniert für jede HSN+TSN-Gruppierung zu behalten
    df = df.loc[idx_to_keep]

    # Sortieren der Rows,primär nach HSN,sekundär nach TSN
    df = df.sort_values(by=['HSN','TSN'])

    # Überprüfen der kombinierten Daten
    print(df.head)
    print(df.columns)
    print(df.info())
    null_rows = df["Co2_kombiniert"].isnull().sum()
    num_duplicates = df.duplicated(subset=["HSN", "TSN"]).sum()
    print(f"Anzahl der Nullwerte in Co2_kombiniert:{null_rows}")
    print(f"Anzahl der Duplikate von HSN und TSN in Kombination :{num_duplicates}")

    # Median der PKW CO2_kombiniert,aber ohne Nullwerte
    median_co2 = df[(df['Fahrzeugtyp'] == 'PKW') & (df['Co2_kombiniert'] != 0)]['Co2_kombiniert'].median()
    print("Median von Co2_kombiniert für PKw (ohne Berücksichtigung von Nullen):", median_co2)

    # Median der LKW CO2_kombiniert, aber ohne Nullwerte
    median_co2 = df[(df['Fahrzeugtyp'] == 'LKW') & (df['Co2_kombiniert'] != 0)]['Co2_kombiniert'].median()
    print("Median von Co2_kombiniert für LKw (ohne Berücksichtigung von Nullen):", median_co2)
    df.to_csv('output_check.csv', index=False)
    return df
