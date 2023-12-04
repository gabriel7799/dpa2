import tabula
import pandas as pd


def parse_from_pdf(file_paths):

# Durchlaufen der Dateipfade und Verarbeitung der PDFs
    for file_path in file_paths:
        # Speichern des DataFrames als CSV-Datei,basierend auf dem Dateinamen,es wurden spezielle Anpassungen für die vorliegenden pdfs vorgenommen  )
        if 'm1' in file_path:
            dfs = tabula.read_pdf(file_path, pages='18-1084', guess=False, area=[150, 15, 790, 550],
                                  columns=[40, 140, 167, 192, 298, 327, 346, 369, 383, 399, 422, 438, 461, 479, 500],
                                  pandas_options={'header': None})
            df = pd.concat(dfs)
            df.to_csv('Kba_emission_2023_Pkw.csv', index=False)
        elif 'n1' in file_path:
            dfs = tabula.read_pdf(file_path, pages='18-347', guess=False, area=[150, 15, 790, 550],
                                  columns=[40, 140, 167, 192, 298, 327, 346, 369, 383, 399, 422, 438, 461, 479, 500],
                                  pandas_options={'header': None})
            df = pd.concat(dfs)
            df.to_csv('Kba_emission_2023_Lkw.csv', index=False)


# area=[150,15,790,550],columns=40,140,167,192,298,327,346,369,383,399,422,438,461,479,500]

# Koordinaten im pdf mit acrobat reader oder safaripdf erfassen
# Koordinatenmaske im pdf, grenzt den eingelesenen Bereich für die Tabelle auf allen Seiten->>> area=[obenlinks-y,obenlinks-x,untenrechts-y,untenrechts-x]
# Kordinatenmaske im pdf, für die Abgrenzung von columns in der Tabelle auf allen Seiten->>> columns[Spaltengrenze1-x,Spaltengrenze2-x,Spaltengranze3-x....]
# wenn Tabellen über mehrere Seiten ausgelesen werden ist pandas_options={'header': None} wichtig da sonst jedes mal die erste row in den header gepackt wird
# um die Koordinatenmaske zu nutzen ist guess=False notwendig

#um tabula in python zu verwenden ist java von Nöten,es muss die PATH-Variable um den Pfad zur java/bin ergänzt werden
