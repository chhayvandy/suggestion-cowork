from pymongo import MongoClient
import pandas as pd
import numpy
from bson import ObjectId
from geopy.distance import great_circle,vincenty
MONGODB_URI = "mongodb://root:root@ds245228.mlab.com:45228/cowork"
client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
db = client.get_database("cowork")
booked_records = db.coworkbooked
cowork_records = db.coworking
def getLong_Latitude():
    records = cowork_records.find()
    return records
def getAllRecode():
    records = booked_records.find()
    return records
def getCoWorkingRecommended(dataRecomment,dataCoWork):
    # print(dataRecomment)
    # print('##########################')
    # print(type(dataCoWork[0]['_id']))
    print(len(dataCoWork))
    listDataRecommendation= []
    for i in dataRecomment:
        # print(type(i))
        for n in range(len(dataCoWork)):
            if str(dataCoWork[n]['_id']) == i:
                listDataRecommendation.append(dataCoWork[n])
                break
    print(listDataRecommendation)
    return listDataRecommendation
def getRECORD(user_id):
    records = booked_records.find_one({"User_ID":user_id})
    return records

def pushRECORD(record):
    booked_records.insert_one(record)

def updateRecord(record, updates):
    booked_records.update_one({'_id': record['_id']},{
                              '$set': updates
                              }, upsert=False)
def suggestionAlgorithm(self):
    dataCoWork = getLong_Latitude()
    listCoWork = []
    listCoWorkID = []
    for i in dataCoWork:
        listCoWork.append(i)
        listCoWorkID.append(str(i['_id']))
    listCoWorkID.sort()
    distance = []
    for i in range(len(listCoWork)):
        distance.append(great_circle((listCoWork[i]['latitude'],listCoWork[i]['longitude']), (self['latitude'],self['longtitude'])).meters/1000)
    dfDistance = pd.DataFrame(distance,columns=['distance'])
    dataUserBooked = getAllRecode()
    listCoWorkBooked = []
    for i in dataUserBooked:
        listCoWorkBooked.append(i)
    dfCoWorkBooked = pd.DataFrame(listCoWorkBooked).sort_values(by=['coworking_id'])
    dfCoWorkBooked = dfCoWorkBooked.reset_index(drop=True)
    listAverageRating = []
    listCountRating   = []
    baseData = dfCoWorkBooked['coworking_id'][0]
    rating   = 0
    countRating = 0
    for i in range(len(dfCoWorkBooked)):
        if dfCoWorkBooked['coworking_id'][i] == baseData :
            if  dfCoWorkBooked['rating'][i]>0 :
                countRating = countRating+1
                rating = dfCoWorkBooked['rating'][i] + rating
            if i < len(dfCoWorkBooked)-1:
                if dfCoWorkBooked['coworking_id'][i+1]!= baseData :
                    baseData = dfCoWorkBooked['coworking_id'][i+1]
                    listAverageRating.append(rating/countRating)
                    listCountRating.append(countRating)
                    rating = 0
                    countRating = 0
            if i == len(dfCoWorkBooked)-1 :
                listAverageRating.append(rating/countRating)
                listCountRating.append(countRating)
    
    dfDistance['coworking_id'] = pd.Series(listCoWorkID)
    dfDistance['count_rating']  = pd.Series(listCountRating)
    dfDistance['average_rating']= pd.Series(listAverageRating)
    C = dfDistance['average_rating'].mean()
    m = dfDistance['count_rating'].quantile(0.50)
    q_movies = dfDistance.copy().loc[dfDistance['count_rating'] >= m]
    q_movies.shape
    def weighted_rating(x, m=m, C=C):
        v = x['count_rating']
        R = x['average_rating']
        return (v/(v+m) * R) + (m/(m+v) * C) 
    q_movies['score'] = q_movies.apply(weighted_rating, axis=1)

    q_movies = q_movies.sort_values('score', ascending=False).head(10).reset_index(drop=True)
    # print(q_movies)
    return q_movies['coworking_id'],listCoWork,q_movies['average_rating']

class getUserLocation():
    def getCoworkingForRecommendation(self) :
        dataForRecomment,dataCoWork,average_rating = suggestionAlgorithm(self)
        dataRecomment = getCoWorkingRecommended(dataForRecomment,dataCoWork)
        dfResultRecomment = pd.DataFrame(dataRecomment)
        # print(dfResultRecomment)
        dfResultRecomment['average_rating'] = average_rating
        print(dfResultRecomment)
        dfResultRecomment['_id'] = dfResultRecomment['_id'].astype(str)
        dfResultRecomment = dfResultRecomment.drop(columns=['details','price_per_hour','approve','rarting'])
        resultForRecomment = dfResultRecomment.to_json(orient='records')
        # print(resultForRecomment)
        return resultForRecomment


