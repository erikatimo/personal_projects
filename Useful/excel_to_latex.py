import pandas as pd

table = pd.read_excel("buying_time_regression.xlsx")

print(table.to_latex(index=False))