# import pandas as pd, numpy as np, pickle, torch
# import requests

# from rest_framework.views import APIView
# from rest_framework.response import Response

# from sentence_transformers import SentenceTransformer
# from sentence_transformers import util
# from openai import OpenAI
# from tqdm.auto import tqdm


# def final_retriever(query, df, retriever, vecs):

#   answer = encoder_df(query, retriever, vecs, df)
#   prompt = prompt_maker(query, answer[0])

#   return prompt, answer[1]



# def prompt_maker(query, top_rows_df):

#   """

#   This function creates prompt that will be fed into chat gpt.

#   New method is aimed to reduce number of tokens by combaining rows with same Sector, Subsector, Indicator combinations.
#   """

#   df_for_prompt = top_rows_df.copy()

#   top_rows_df['sec_subs_indctr'] = 'Sector: ' + top_rows_df['Sector'] + ', Subsector: ' + top_rows_df['Subsector'] + ', Indicator: ' + top_rows_df['Indicator']

#   top_rows_np = top_rows_df.values

#   N = top_rows_df['sec_subs_indctr'].nunique()
#   M = top_rows_df.shape[0]

#   if N < M*0.4:
#     prompt = query + '\n\nFind the answer from the table below:\n\n'
#     unique_headers = top_rows_df['sec_subs_indctr'].unique()
#     for header in unique_headers:
#       prompt += '\n\n' + header + ':\nYear, Country, Country Code, Amount, Rank\n'
#       rows = '\n'.join([str(row[0]) + ' ' + row[4] + ' ' + row[5] + ' ' + str(row[6]) + ' ' + str(row[7]) for row in top_rows_df.values if row[-1] == header])
#       prompt += rows

#   else:
#     prompt = query + '\n\nFind the answer from the table below:\n\n' + 'Year, Sector, Subsector, Indicator, Country, Country Code, Amount, Rank\n\n'
#     prompt += '\n'.join(['(' + ', '.join(str(element) for element in row) + ')' for row in df_for_prompt.values])

#   return prompt

# def encoder_df(query, retriever, vecs, df, top_n_rows=50):

#     """
#     Function Inputs: User query, Sentence Transformer, Embeddings, dataframe, number of top rows (default = 50)
#     Function Output: Prompt given to ChatGPT and average of cosine similarity scores of top 50 rows.

#     Function takes user input query and converts in into vector embedding (pay attention to use same transformer for both df encoding and query encoding).
#     After that, similarity score between query and dataframe embeddings are calculated.
#     The scores are sorted in descending order and indexes of top 50 scores are taken.
#     The indexes are used to select rows from pandas dataframe.

#     After having 50 rows, it is converted into tuple like strings and combined with other prompt to feed ChatGPT final string.

#     Also, mean (average) of top 50 scores are calucalted and returned together with prompt.

#     """

#     query_embedding = retriever.encode(query)
#     scores = util.pytorch_cos_sim(vecs, query_embedding).squeeze()

#     top_indices = np.argsort(-scores)[:top_n_rows]
#     top_scores = scores[top_indices]
#     average_top_50 = torch.mean(top_scores)

#     col_names = df.columns
#     top_rows_np = df.values[top_indices]

#     for i in range(top_rows_np.shape[0]):
#       top_rows_np[i, -2] = np.round(top_rows_np[i, -2], 1)

#     top_rows = df.values[top_indices]
#     top_rows_df = pd.DataFrame(top_rows_np, columns = col_names)

#     return top_rows_df, average_top_50


# class ChatBotAPIView(APIView):
#     def post(self, request):
#         device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
#         df = pd.read_csv('updated_searchart_data (1) (1).csv')
#         print(df)
#         retriever = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device = device)
#         message = request.data.get('message')
#         print(message)
#         messages = [{'role':'system', 'content':""" This is chatbot for a project. I have over 1 million rows of dataset and
#                                            I have built a model to return 50 rows which are the most suitable for answering the query asked by the user.
#                                            Now, I will give you the query and those 50 rows to return me the final answer to the question. For answering, use
#                                            only the data I have provided you which is 50 rows. Do not use any other data. Also, do not make comments about the answer,
#                                            only return the answer to the question.  """}]

#         with open('encoded_data.pkl', "rb") as file:
#             embeddings = pickle.load(file)

#         # message = input('User : ')
#         ans = final_retriever(message, df, retriever, embeddings)
        
#         # print(ans[0])
#         if ans[1].item() > 0.45:
#             print(message)
#             message = ans[0]
#         else:
#             message = message
#         if message:
#             messages.append(
#                 {'role':'user', 'content':message},
#             )
#             client = OpenAI(api_key="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")
#             chat = client.chat.completions.create(
#                 model = 'gpt-3.5-turbo', messages = messages, temperature = 0.7
#             )
#         reply = chat.choices[0].message.content

#         return Response({"message": reply})