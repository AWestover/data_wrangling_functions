# A compilation of all of my xls functions (should work for xlsx too...)

# libraries
import pandas as pd


# functions


# turns a xls into a csv for every sheet
# give a location for it to dump all of the csvs
# if the sheets have headers pass headers_included=True
def xls_to_csvs(new_folder: str, xls_file_loc: str):
    try:
        excel_file = pd.ExcelFile(xls_file_loc)
        for sheet in excel_file.sheet_names:
            cur_sheet = excel_file.parse(sheet)
            cur_sheet.to_csv(new_folder + "/" + sheet + '.csv', index=False)
    except PermissionError:
        print("Please close the the file I can't access it while you have it open")

xls_to_csvs('data', 'data/test.xlsx')
