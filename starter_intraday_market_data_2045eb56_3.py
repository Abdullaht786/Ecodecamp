# -*- coding: utf-8 -*-
"""Starter: Intraday market data 2045eb56-3

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/#fileId=https%3A//storage.googleapis.com/kaggle-colab-exported-notebooks/starter-intraday-market-data-2045eb56-3-35bac10a-d52c-4d22-84ad-07d1dfd66e8f.ipynb%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com/20241015/auto/storage/goog4_request%26X-Goog-Date%3D20241015T054649Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D02c2219ba00d98afc74c97ca746f1a237601739c346a6ce01bc3c066c6153da3099ac89bbebf13fb52ec286625c7ba54996a7cd8e1654507a2f7149f4b5f778d54b9f0b44dedcd3209b3d6b165c76de4db582ddcdcb08bdc6e6a2a0101ffa8a97e98e0099ee604de4234acf05912added6c919ed66b88a14e5a4f2b7daeb6bcdfefdfcdcc35b3ff380ea28a7ce8f0e853caf6fd02b7f9182f280979f14da2fbaa2249c8d3473cdb7c4574909ac0441cdc05b9be9c1c010d0130d47caa5b492b553f2d6f9a8df5164bb777902cbceb36e4fe9829620fbc5a3828a5a2b4490d98fa5ff2a420155ddd604f3e4f40f1f24ed721f3ef3f0027ad78fee38192c795c3a

## Exploratory Analysis
To begin this exploratory analysis, first import libraries and define functions for plotting the data using `matplotlib`. Depending on the data, not all plots will be made. (Hey, I'm just a simple kerneling bot, not a Kaggle Competitions Grandmaster!)
"""

from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

"""There are 17 csv files in the current version of the dataset:

"""

for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

"""The next hidden code cells define functions for plotting data. Click on the "Code" button in the published kernel to reveal the hidden code."""

# Distribution graphs (histogram/bar graph) of column data
def plotPerColumnDistribution(df, nGraphShown, nGraphPerRow):
    nunique = df.nunique()
    df = df[[col for col in df if nunique[col] > 1 and nunique[col] < 50]] # For displaying purposes, pick columns that have between 1 and 50 unique values
    nRow, nCol = df.shape
    columnNames = list(df)
    nGraphRow = (nCol + nGraphPerRow - 1) / nGraphPerRow
    plt.figure(num = None, figsize = (6 * nGraphPerRow, 8 * nGraphRow), dpi = 80, facecolor = 'w', edgecolor = 'k')
    for i in range(min(nCol, nGraphShown)):
        plt.subplot(nGraphRow, nGraphPerRow, i + 1)
        columnDf = df.iloc[:, i]
        if (not np.issubdtype(type(columnDf.iloc[0]), np.number)):
            valueCounts = columnDf.value_counts()
            valueCounts.plot.bar()
        else:
            columnDf.hist()
        plt.ylabel('counts')
        plt.xticks(rotation = 90)
        plt.title(f'{columnNames[i]} (column {i})')
    plt.tight_layout(pad = 1.0, w_pad = 1.0, h_pad = 1.0)
    plt.show()

# Correlation matrix
def plotCorrelationMatrix(df, graphWidth):
    filename = df.dataframeName
    df = df.dropna('columns') # drop columns with NaN
    df = df[[col for col in df if df[col].nunique() > 1]] # keep columns where there are more than 1 unique values
    if df.shape[1] < 2:
        print(f'No correlation plots shown: The number of non-NaN or constant columns ({df.shape[1]}) is less than 2')
        return
    corr = df.corr()
    plt.figure(num=None, figsize=(graphWidth, graphWidth), dpi=80, facecolor='w', edgecolor='k')
    corrMat = plt.matshow(corr, fignum = 1)
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.gca().xaxis.tick_bottom()
    plt.colorbar(corrMat)
    plt.title(f'Correlation Matrix for {filename}', fontsize=15)
    plt.show()

# Scatter and density plots
def plotScatterMatrix(df, plotSize, textSize):
    df = df.select_dtypes(include =[np.number]) # keep only numerical columns
    # Remove rows and columns that would lead to df being singular
    df = df.dropna('columns')
    df = df[[col for col in df if df[col].nunique() > 1]] # keep columns where there are more than 1 unique values
    columnNames = list(df)
    if len(columnNames) > 10: # reduce the number of columns for matrix inversion of kernel density plots
        columnNames = columnNames[:10]
    df = df[columnNames]
    ax = pd.plotting.scatter_matrix(df, alpha=0.75, figsize=[plotSize, plotSize], diagonal='kde')
    corrs = df.corr().values
    for i, j in zip(*plt.np.triu_indices_from(ax, k = 1)):
        ax[i, j].annotate('Corr. coef = %.3f' % corrs[i, j], (0.8, 0.2), xycoords='axes fraction', ha='center', va='center', size=textSize)
    plt.suptitle('Scatter and Density Plot')
    plt.show()

"""Now you're ready to read in the data and use the plotting functions to visualize the data.

### Let's check 1st file: /kaggle/input/ES - week ending 2020 02 01.csv
"""

nRowsRead = 1000 # specify 'None' if want to read whole file
# ES - week ending 2020 02 01.csv may have more rows in reality, but we are only loading/previewing the first 1000 rows
df1 = pd.read_csv('/kaggle/input/ES - week ending 2020 02 01.csv', delimiter=',', nrows = nRowsRead)
df1.dataframeName = 'ES - week ending 2020 02 01.csv'
nRow, nCol = df1.shape
print(f'There are {nRow} rows and {nCol} columns')

"""Let's take a quick look at what the data looks like:"""

df1.head(5)

"""Distribution graphs (histogram/bar graph) of sampled columns:"""

plotPerColumnDistribution(df1, 10, 5)

"""Correlation matrix:"""

plotCorrelationMatrix(df1, 8)

"""Scatter and density plots:"""

plotScatterMatrix(df1, 6, 15)

"""### Let's check 2nd file: /kaggle/input/TOS Kaggle data week ending 2020 02 01/TOS Kaggle data week ending 2020 02 01/XTN - week ending 2020 02 01.csv"""

nRowsRead = 1000 # specify 'None' if want to read whole file
# XTN - week ending 2020 02 01.csv may have more rows in reality, but we are only loading/previewing the first 1000 rows
df2 = pd.read_csv('/kaggle/input/TOS Kaggle data week ending 2020 02 01/TOS Kaggle data week ending 2020 02 01/XTN - week ending 2020 02 01.csv', delimiter=',', nrows = nRowsRead)
df2.dataframeName = 'XTN - week ending 2020 02 01.csv'
nRow, nCol = df2.shape
print(f'There are {nRow} rows and {nCol} columns')

"""Let's take a quick look at what the data looks like:"""

df2.head(5)

"""Distribution graphs (histogram/bar graph) of sampled columns:"""

plotPerColumnDistribution(df2, 10, 5)

"""Correlation matrix:"""

plotCorrelationMatrix(df2, 8)

"""Scatter and density plots:"""

plotScatterMatrix(df2, 6, 15)

"""### Let's check 3rd file: /kaggle/input/TOS Kaggle data week ending 2020 02 01/TOS Kaggle data week ending 2020 02 01/example data - week ending 2020 02 01.csv"""

nRowsRead = 1000 # specify 'None' if want to read whole file
# example data - week ending 2020 02 01.csv may have more rows in reality, but we are only loading/previewing the first 1000 rows
df3 = pd.read_csv('/kaggle/input/TOS Kaggle data week ending 2020 02 01/TOS Kaggle data week ending 2020 02 01/example data - week ending 2020 02 01.csv', delimiter=',', nrows = nRowsRead)
df3.dataframeName = 'example data - week ending 2020 02 01.csv'
nRow, nCol = df3.shape
print(f'There are {nRow} rows and {nCol} columns')

"""Let's take a quick look at what the data looks like:"""

df3.head(5)

"""Distribution graphs (histogram/bar graph) of sampled columns:"""

plotPerColumnDistribution(df3, 10, 5)

"""Correlation matrix:"""

plotCorrelationMatrix(df3, 8)

"""Scatter and density plots:"""

plotScatterMatrix(df3, 20, 10)

"""## Conclusion
This concludes your starter analysis! To go forward from here, click the blue "Fork Notebook" button at the top of this kernel. This will create a copy of the code and environment for you to edit. Delete, modify, and add code as you please. Happy Kaggling!
"""