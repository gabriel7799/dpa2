from parse_from_pdf import parse_from_pdf
from dataprocessor import process_data
from db_loader import load_db


def data_main():
    file_paths = ["sv222_m1_kraft_pdf.pdf", "sv232_n1_kraft_pdf.pdf"]

    #parse_from_pdf(file_paths)

    csv_paths=['Kba_emission_2023_Pkw.csv','Kba_emission_2023_Lkw.csv']

    df=process_data(csv_paths)

    load_db(df)


data_main()

