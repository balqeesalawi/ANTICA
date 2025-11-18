import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from main.models import Auction  # move import here
        self.auction_id = self.scope['url_route']['kwargs']['auction_id']
        self.room_group_name = f'auction_{self.auction_id}'

        # Join auction group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Send current bid
        auction = await database_sync_to_async(Auction.objects.get)(id=self.auction_id)
        await self.send(text_data=json.dumps({
            'bid': float(auction.current_price),
            'bidder': None
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        from main.models import Auction  # import here if needed
        data = json.loads(text_data)
        amount = data['amount']
        user = self.scope['user'].username

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'bid_message',
                'bid': amount,
                'bidder': user
            }
        )

    async def bid_message(self, event):
        await self.send(text_data=json.dumps({
            'bid': event['bid'],
            'bidder': event['bidder']
        }))
