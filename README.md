################## 21-08-2025 code ##################

# cwd = os.getcwd()  # Get the current working directory (cwd)
# files = os.listdir(cwd)

# print(files)
# import pandas as pd

# # Read file excel
# df = pd.read_excel('/Users/Phinconers/Desktop/folder 2025/Dokumen Ryo/Udemy Math Foundation/object-classification/object.xlsx')

# grouped = df.groupby('Type')['Object Name'].agg(lambda x: ' OR '.join(x.unique())).reset_index()

# # Save file excel
# grouped.to_excel('/Users/Phinconers/Desktop/folder 2025/Dokumen Ryo/Udemy Math Foundation/object-classification/grouped.xlsx', index=False)

# print(grouped)