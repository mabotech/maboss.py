

from flask.views import MethodView

class UserAPI(MethodView):
    
    def all(self):
        
        return "all 2"
        
    def one(self, user_id):
        
        return "user 2: %s" % (user_id)

    def get(self, user_id=None):
        if user_id is None:
            # return a list of users
            pass
            #return "list"
            return self.all()
        else:
            # expose a single user
            pass
            return self.one(user_id)
            #return "user1:%s" % (user_id)

    def post(self):
        # create a new user
        pass

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass