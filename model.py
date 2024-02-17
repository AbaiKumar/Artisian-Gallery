from bson import ObjectId
from pymongo import MongoClient


class Data:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.database = self.client["Art_Gallery"]
        self.userCollectiona = self.database["Usersa"]
        self.userCollectionc = self.database["Usersc"]
        self.productCollection = self.database["Products"]
        
    def ar(self,query):
        self.productCollection.insert_one(query)
        return True
    
    def createAccountc(self, mail, password):
        user_document = {
            "mail": mail,
            "password": password
        }
        if (self.userCollectionc.find_one({"mail": mail}) == None):
            self.userCollectionc.insert_one(user_document)
            return True
        else:
            return False
        
    def addartist(self, query, mail):
        u = self.userCollectiona.find_one({"mail": mail})
        if u:
            self.userCollectiona.update_one({"mail": mail}, {"$set": query})
            return True
        else:
            return False

    
    def createAccounta(self, mail, password):
        user_document = {
            "mail": mail,
            "password": password
        }
        if (self.userCollectiona.find_one({"mail": mail}) == None):
            self.userCollectiona.insert_one(user_document)
            return True
        else:
            return False

    def loginAccount(self, mail, pwd):
        query = {"mail": mail}
        result = self.userCollectionc.find_one(query)

        if result:
            if result.get("password") == pwd:
                return 1
            
        result1 = self.userCollectiona.find_one(query)
        if result1:
            if result1.get("password") == pwd:
                return 2
        return 3

    def getData(self, indx):
        try:
            start = indx * 10
            end = start + 10
            data = list(self.productCollection.find(
                {}, {'_id': 1, 'title': 1, 'des': 1, 'sell_type': 1,'price':1,'art':1, 'discount':1}).skip(start).limit(end))
            for item in data:
                item['_id'] = str(item['_id'])
            return [True, data]
        except Exception as e:
            return [False, []]

    def getSingle(self, pid):
        obj_pid = ObjectId(pid)
        try:
            data = list(self.productCollection.find({"_id": obj_pid}))
            data[0]['_id'] = str(data[0]['_id'])
            return [True, data[0]]
        except:
            return [False, []]

    def addItemToCart(self, itemID, mail):
        print(itemID)
        print(mail)
        user_document = {"mail": mail}
        user_result = self.userCollectionc.find_one(user_document)

        if user_result is None:
            return False
        else:
            update_result = self.userCollectionc.update_one(
                {"mail": mail},
                {"$set": {f"checkout.{itemID}": 1, "placed": {}}},
                upsert=True
            )

            if update_result.modified_count > 0 or update_result.upserted_id is not None:
                return True
            else:
                return False

    def getItemFromCart(self, mail):
        user_document = {"mail": mail}
        user_result = self.userCollectionc.find_one(user_document)
        productList = []

        if user_result is None:
            return {"data": productList, "msg": False}
        else:
            for id, quantity in user_result["checkout"].items():
                data = self.productCollection.find_one({"_id": ObjectId(id)})
                product = {"id": str(data["_id"]), "Name": data["name"], "Price": data["price"],
                           "Discount": data["discount"], "Quantity": quantity}
                productList.append(product)
            return {"data": productList, "msg": True}

    def updateCheckoutData(self, record, mail):
        user_document = {"mail": mail}
        user_result = self.userCollection.find_one(user_document)
        if user_result is None:
            return False
        else:
            for i in record:
                if user_result['checkout'][i['id']] != i["Quantity"]:
                    print("hi")
                    update_result = self.userCollection.update_one(
                        {"mail": mail},
                        {"$set": {f"checkout.{i['id']}": int(i["Quantity"])}},
                        upsert=True
                    )

                    if update_result.modified_count > 0 or update_result.upserted_id is not None:
                        continue
                    else:
                        return False
        return True


data = Data()
