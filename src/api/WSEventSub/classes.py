class SubscriptionType():
    Fields = {'target': 'broadcaster_user_id', 
              'self': 'moderator_user_id'}
    Version = 1
    Type = "Base"
    
class Follow(SubscriptionType):
    Type = 'channel.follow'
    Version = 2

class Subscribe(SubscriptionType):
    Type = 'channel.subscribe'
    Version = 1

class Resubscribe(SubscriptionType):
    Type = 'channel.subscription.message'
    Version = 1



