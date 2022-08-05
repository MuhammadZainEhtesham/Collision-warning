from pymongo import MongoClient

def getuser_id(liscence_plate):
    cluster = MongoClient("mongodb+srv://zainEhtesham:capslockonkrk@testcluster.tihct.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster.test
    collection = db['assigned_drivers']
    doc = collection.find_one({'liscence_plate':liscence_plate})
    user_id = (doc['user_id'])
    return user_id

def get_doc(user_id):
    cluster = MongoClient("mongodb+srv://zainEhtesham:capslockonkrk@testcluster.tihct.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster.test
    collection = db['score_hist']
    doc = collection.find_one({'user_id':user_id})
    return doc

def update_doc(user_id,score):
    cluster = MongoClient("mongodb+srv://zainEhtesham:capslockonkrk@testcluster.tihct.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster.test
    collection = db['score_hist']
    myquery1 = {'user_id':user_id}
    new_value1 = {"$set":{'cb_score':score}}
    myquery2 = {'user_id':user_id}
    new_value2 = {"$push":{'cb_score_list':score}}
    collection.update_one(myquery1,new_value1)
    collection.update_one(myquery2,new_value2)

def update_properties(liscence_plate,score):
    user_id = getuser_id(liscence_plate)
    #update driver's properties
    update_doc(str(user_id),score)
