##############################################################################
        ##### RELATIONSHIP TABLE FOR USER AND POSTCARD ####
        ### records users states they have visited  ###
##############################################################################

class UserPostcard(db.Model):
    """user upload their picture and send it to social media"""

    __tablename__ = "user_postcards"

    user_postcard_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.ForeignKey('postcards.user_id'))
    postcard_id = db.Column(db.Integer, db.ForeignKey('postcards.postcard_id'))

    #Define the relationship to user
    user = db.relationship("UserPostcard", backref=db.backref("user", order_by=userpostcard.user_id))
    #Define the relationship to user table
    postcard = db.relationship("Postcard", backref=db.backref("user_postcards.postcard_id", order_by=postcards.postcard_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Postcard user_postcard_id=%s user_id=%s postcard_id>" % (self.user_postcard_id, self.user_id, postcard_id,)





