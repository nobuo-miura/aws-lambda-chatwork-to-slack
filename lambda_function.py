import json
import os
import requests
from datetime import datetime

def lambda_handler(event, context):
    chatwork_token = event['chatwork_token']
    chatwork_room_id = event['chatwork_room_id']
    slack_webhook_url = event['slack_webhook_url']

    url = "https://api.chatwork.com/v2/rooms/" + chatwork_room_id +"/messages"
    headers = {
        "accept": "application/json",
        "x-chatworktoken": chatwork_token
    }

    chatwork_response = requests.get(url, headers=headers)
    if chatwork_response.status_code == 204 :
        print('204 Empty Response.' )
    else : 
        messages = chatwork_response.json()
      
        for message in messages:
            body = message['body']
            name = message['account']['name']
            msid = message['message_id']
            time = message['send_time']
            text = '*' + str(datetime.fromtimestamp(time)) + ' message from: ' + name + '*\n```' + body + '```'
         
            slack_message = {
                'text': text
            }
            requests.post(slack_webhook_url, data=json.dumps(slack_message), headers={'Content-Type': 'application/json'})
    
    return {
        'statusCode': 200,
        'body': json.dumps('Messages transferred successfully')
    }