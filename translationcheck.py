# %%
# Imports the Google Cloud client library
import pandas as pd
from google.cloud import translate
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:\devsbb\workspaces\\3laenderhack19\poc-cia-a0819b9acb7b.json"

# Instantiates a client
translate_client = translate.Client()

# # The target language
# target = 'de'
# source = 'en'

# # Translates some text into Russian
# translation = translate_client.translate(
#     ["Hello", "World"],
#     target_language=target,
#     source_language=source)

# %%
df = pd.DataFrame(translation)


# %%


def translate_list(series, source_language, target_language):
    segments = [series[:100], series[100:200], series[200:]]
    return sum([translate_chunk(chunk, source_language, target_language)
                for chunk in segments], [])


def translate_chunk(chunk, source_language, target_language):
    translation = pd.DataFrame(translate_client.translate(
        chunk, source_language=source_language, target_language=target_language))
    return translation['translatedText'].values.tolist()


def translate_language(input, source_col, source_language, target_languages):
    for target_language in target_languages:
        result = translate_list(input[source_col].values.tolist(),
                                source_language=source_language, target_language=target_language)
        input["%s2%s" % (source_language, target_language)] = result


# %%
input = pd.read_excel('./KorrigiertesDictionary.xlsx')
translate_language(input, 'Railway word/phrase - English', 'en', ['de', 'hu'])
translate_language(input, 'German (ÖBB)', 'de', ['en', 'hu'])
translate_language(input, 'Hungarian (MAV)', 'hu', ['en', 'de'])

# %%
input = input.apply(lambda x: x.astype(str).str.lower())

# %%
input.to_excel('./google-translate-vergleich.xlsx')
input.to_csv('./google-translate-vergleich.csv')
