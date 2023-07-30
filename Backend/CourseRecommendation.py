import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


data = pd.read_csv('coursea_data.csv')
data2 = data.iloc[:,[1,2,3,4,5,6,7]]
data2 = pd.DataFrame(data2)

print(data2.columns)

data2['descriptions'] = data2['course_title'] + ' ' + data2['course_Certificate_type'] + ' ' + data2['course_difficulty'] + ' ' + data2['Description']
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(data2['descriptions'])

def get_course_recommendation(user_interest, cosin_matrix, df):
    user_tfidf = tfidf_vectorizer.transform([user_interest])

    score = cosine_similarity(user_tfidf, tfidf_matrix)
    score = score[0]

    score = list(enumerate(score))
    score = sorted(score,key=lambda x:x[1],reverse=True)
    course_index = [i[0] for i in score]
    return df['course_title'].iloc[course_index[:3]]



def get_recommendation(user_interest):
    return get_course_recommendation(user_interest, cosine_similarity, data2)

if __name__ == '__main__':
    user_interest = input("Enter the output from quiz")

    recommendation = get_course_recommendation(user_interest,cosine_similarity, data2)
    print("Recommended courses are:")
    print(recommendation)

