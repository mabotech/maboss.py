
#
def get(uid=None):
    if uid is None:
        return index()
    else:
        # expose a single user
        return one(uid)

#
def index():
    
    return "list2000"

#
def one(uid):
    
    return "2333:%s" %(uid)

#
def post():
    # create a new user
    return "post"

#
def delete(uid):
    # delete a single user
    return "delete"

#
def put(self, uid):
    # update a single user
    return "put"