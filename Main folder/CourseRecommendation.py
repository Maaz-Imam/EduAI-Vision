import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


data = pd.read_csv('courses.csv')
data2 = data.iloc[:,[1,2,3,4,5,6,7]]
data2 = pd.DataFrame(data2)

print(data2.columns)

data2['descriptions'] = data2['course_title'] + ' ' + data2['course_Certificate_type'] + ' ' + data2['course_difficulty'] + ' ' + data2['Description']
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(data2['descriptions'])

'''
tf_idf score = (term frequency) * (inverse document frequency)
tf: relative frequency of term t within document d
idf: measures how much information the word provides, that is,
if the word is common or rare across all documents. For example, 
'the' is too common, so we will want its idf to be small.
'''

def get_course_recommendation(user_interest, cosin_matrix, df):
    user_tfidf = tfidf_vectorizer.transform([user_interest])

    score = cosine_similarity(user_tfidf, tfidf_matrix)
    score = score[0]

    score = list(enumerate(score))
    score = sorted(score,key=lambda x:x[1],reverse=True)
    course_index = [i[0] for i in score]
    course_names = ", ".join(df['course_title'].iloc[course_index[:3]])
    enumerated_names = "\n".join(f" {i+1}. {name}" for i, name in enumerate(course_names.split(", ")))
    return f"Your recommended courses are:\n{enumerated_names}"


def get_recommendation(user_interest):
    return get_course_recommendation(user_interest, cosine_similarity, data2)

def courseRecommender(user_interest):
    recommendation = get_course_recommendation(user_interest,cosine_similarity, data2)
    print(recommendation)
    return recommendation

if __name__ == '__main__':
    user_interest = input("Enter the output from quiz")

    recommendation = get_course_recommendation(user_interest,cosine_similarity, data2)
    print("Recommended courses are:")
    print(recommendation)

