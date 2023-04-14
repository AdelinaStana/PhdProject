import pandas as pd


class CsvConverter:
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2

    def convert(self):
        df1 = pd.read_csv(self.file1)
        df2 = pd.read_csv(self.file2)

        names = pd.concat([df1.iloc[:, :2], df2.iloc[:, :2]]).drop_duplicates()
        name_to_id = {name: i for i, name in enumerate(names.iloc[:, 0])}

        df1.iloc[:, :2] = df1.iloc[:, :2].applymap(lambda x: name_to_id[x])
        df2.iloc[:, :2] = df2.iloc[:, :2].applymap(lambda x: name_to_id[x])

        df1.to_csv(self.file1.split('.')[0] + '_converted.csv', index=False)
        df2.to_csv(self.file2.split('.')[0] + '_converted.csv', index=False)
