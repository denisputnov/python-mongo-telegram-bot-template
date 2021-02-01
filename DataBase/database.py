from pymongo import MongoClient

class DataBase:
    def __init__(self, db_user, db_password, db_name):
        self._cluster = MongoClient(f'mongodb+srv://{db_user}:{db_password}@cluster0.gafny.mongodb.net/{db_name}?retryWrites=true&w=majority')
        self._db = self._cluster[db_name]

        self._users_collection = self._db['users']

        self._db_user = db_user
        self._db_password = db_password
        self._db_name = db_name
        print('db inited successfully')
    

    def subscribe_user(self, message):
        try:
            # add user if user is not in collection
            if self._users_collection.count_documents({'_id': message.from_user.id}) == 0:
                self._users_collection.insert_one({
                    '_id': message.from_user.id,
                    'username': message.chat.username,
                    'first_name': message.from_user.first_name,
                    'last_name': message.from_user.last_name,
                    'isSubscribed': True,
                })
            # update user status if user is in collection
            else:
                self._users_collection.update_one({'_id': message.from_user.id}, {'$set': {'isSubscribed': True},},)
            
            # return True if operation is done
            return True

        except Exception as error:
            # return False if operation is not done
            print(error)
            return False


    def unsubscribe_user(self, message):
        try:
            # add user if user is not in collection
            if self._users_collection.count_documents({'_id': message.from_user.id}) == 0:
                self._users_collection.insert_one({
                    '_id': message.from_user.id,
                    'username': message.chat.username,
                    'first_name': message.from_user.first_name,
                    'last_name': message.from_user.last_name,
                    'isSubscribed': False,
                })
            # update user status if user is in collection
            else:
                self._users_collection.update_one({'_id': message.from_user.id}, {'$set': {'isSubscribed': False},},)
            
            # return True if operation is done
            return True

        except Exception as error:
            # return False if operation is not done
            print(error)
            return False
            

    def register_user(self, message):
        try:
        # if user is not registered
            if self._users_collection.count_documents({'_id': message.from_user.id}) == 0:
                self._users_collection.insert_one({
                    '_id': message.from_user.id,
                    'username': message.chat.username,
                    'first_name': message.from_user.first_name,
                    'last_name': message.from_user.last_name,
                    'isSubscribed': False,
                })
            # if user were registered before
            else: 
                print(f'Tried to register user(_id: {message.from_user.id}), but he were registered before.')

            # return True if operation is done
            return True

        except Exception as error:
            # return False if operation is not done
            print(error)
            return False


    def get_all_users(self):
        return list(self._users_collection.find())
    

    def get_all_users_identificators(self): 
        users = list(self._users_collection.find())
        return [user['_id'] for user in users]

