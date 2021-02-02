from pymongo import MongoClient


class DataBase:
    """
    - register_user(message)
    - subscribe_user(message)
    - unsubscribe_user(message)
    - check_subscription_status_for_user(user_id)
    - get_all_users_data()
    - get_subscribed_users_data()
    - get_all_users_identificators()
    - get_subscribed_users_identificators()
    - get_subscription_stats()
    """

    def __init__(self, connection_string, db_name):
        self._cluster = MongoClient(connection_string)
        self._db = self._cluster[db_name]

        self._users_collection = self._db['users']

        self._db_name = db_name

        print('db inited successfully')
    

    def register_user(self, message):
        """ 
        register user in the colelction[users] in the format: 
        {
            '_id': message.from_user.id,
            'username': message.chat.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'isSubscribed': False,
        }
        """
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


    def subscribe_user(self, message):
        """ 
        subscribe user in the collection[users]
        if user is not in the collection, add user in the format:
        {
            '_id': message.from_user.id,
            'username': message.chat.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'isSubscribed': True,
        }
        if user is alreary in the collection, change user field "isSubscribed" = True
        """
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
        """ 
        unsubscribe user from the collection[users]
        if user is not in the collection, add user in the format:
        {
            '_id': message.from_user.id,
            'username': message.chat.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'isSubscribed': False,
        }
        if user is alreary in the collection, change user field "isSubscribed" = False
        """
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
            

    def check_subscription_status_for_user(self, user_id):
        """
        Check user subscription status;
        return True/False values;
        """
        try:
            return self._users_collection.find_one({"_id": user_id})['isSubscribed'] 

        except Exception as error:
            print(error)


    def get_all_users_data(self):
        """
        return users list with all data from collection[users]
        list(dict(), dict(), dict(),...)
        """
        try:
            return list(self._users_collection.find())

        except Exception as error:
            print(error)
    

    def get_subscribed_users_data(self):
        """
        return users list with all data from collection[users] for subscriber users [isSubscribed == True]
        list(dict(), dict(), dict(),...)
        """
        try: 
            users = self.get_all_users_data()
            return [user for user in users if user['isSubscribed'] == True]

        except Exception as error:
            print(error)


    def get_all_users_identificators(self): 
        """
        return list with only users identificators from collection[users]
        lust(int, int, int,...)
        """
        try: 
            users = list(self._users_collection.find())
            return [user['_id'] for user in users]

        except Exception as error:
            print(error)


    def get_subscribed_users_identificators(self):
        """
        return list with only users identificators from collection[users] for subscriber users [isSubscribed == True]
        lust(int, int, int,...)
        """
        try:
            users = self.get_all_users_data()
            return [user['_id'] for user in users if user['isSubscribed'] == True]

        except Exception as error:
            print(error)


    def get_subscription_stats(self):
        """
        return {
            'percentage': [float] value from 0 to 1 which means percentage of subscription by users
            'subscribed': [int] amount of subscribed users,
            'total': [int] total amount of interacted users,
        }
        """
        try: 
            users = self.get_all_users_data()
            subscribed = len([user for user in users if user['isSubscribed'] == True])
            total = len(users)

            return {
                'percentage': subscribed / total,
                'subscribed': subscribed,
                'total': total,
            }

        except Exception as error:
            print(error)
