

class Activity(object):

    def text(self):
        pass

    def data(self):
        pass


class VotePassageActivity(Activity):

    type = 'vote.passage'

    def __init__(self, obj, subscriber):
        self.obj = obj
        self.subscriber = subscriber

    def text(self):

        voted_count = 0
        for_count = 0
        against_count = 0

        for legislator_id in self.subscriber.followed_legislators():

            lv = self.obj['voters'][legislator_id]
            vote = lv.get('vote')

            if vote == 'Yea':
                for_count += 1
            elif vote == 'Nay':
                against_count += 1

            if vote != 'Not Voting':
                voted_count += 1

        return None

    def data(self):

        votes = {}

        for legislator_id in self.subscriber.followed_legislators():

            lv = self.obj['voters'][legislator_id]

            if lv.get('vote') != 'Not Voting':
                voted_count += 1

            votes[legislator_id] = lv.get('vote')

        return {'roll_call': self.obj, 'followed_legislators': votes}



class BillIntroductionActivity(Activity):

    type = 'bill.introduction'

    def __init__(self, bill, subscriber):
        pass


FEED_ACTIVITIES = [VotePassageActivity, BillIntroductionActivity]
NOTIFICATION_ACTIVITIES = [VotePassageActivity, BillIntroductionActivity]
