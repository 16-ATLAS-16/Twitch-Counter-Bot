class SubscriptionType():
    Fields = {'target': 'broadcaster_user_id', 
              'self': 'moderator_user_id'}
    Version = 1
    Type = "Base"
    
class Follow(SubscriptionType):
    Type = 'channel.follow'
    Version = 2




