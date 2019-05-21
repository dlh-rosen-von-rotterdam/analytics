# %%
import pandas as pd

# %%
input = pd.read_excel('./KorrigiertesDictionary.xlsx')

# %%
input[['Railway word/phrase - English',
       'German (ÖBB)']].to_csv('en_de.tsv', sep='\t', header=False, index=False)
