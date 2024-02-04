from celery import shared_task
from django.contrib.auth import get_user_model
from api.models import Event
from twilio.rest import Client
from decouple import config
from .constants import EVENT_MESSAGES as event_messages
 

@shared_task
def send_event_notification(event_id,request_type):
    print("event recived")
    if request_type=="DELETE":
        try:
            # if the event is deleted means we are not able to query db so passed the Details as a dict
            users_with_mobile_numbers = get_user_model().objects.exclude(phone_number__isnull=True)
            # Send SMS notifications to each user
            for user in users_with_mobile_numbers:
                
                send_sms_notification(user.phone_number, event_id["title"],event_id["date"],event_id["time"],event_id["location"],request_type)

            return None
    
        except Exception as e:
            print(f"Error sending event notification SMS: {e}")
    else:  
        try:
                # Retrieve the event
                event = Event.objects.get(id=event_id)
                users_with_mobile_numbers = get_user_model().objects.exclude(phone_number__isnull=True)
                # Send SMS notifications to each user
                for user in users_with_mobile_numbers:
                    send_sms_notification(user.phone_number, event.title,event.date,event.time,event.location,request_type)

                return None
        except Event.DoesNotExist:
            print(f"Event with id {event_id} does not exist.")
        except Exception as e:
            print(f"Error sending event notification SMS: {e}")

def send_sms_notification(phone_number, event_title,event_date,event_time,event_location,request_type):
    twilio_account_sid = config('TWILIO_ACCOUNT_SID')
    twilio_auth_token = config('TWILIO_AUTH_TOKEN')
    twilio_phone_number = config('TWILIO_PHONE_NUMBER')

    client = Client(twilio_account_sid, twilio_auth_token)

    event_create_message_body = event_messages.get('create', '').format(
        event_title=event_title,
        event_date=event_date,
        event_time=event_time,
        event_location=event_location
    )
    event_update_message_body = event_messages.get('update', '').format(
        event_title=event_title,
        event_date=event_date,
        event_time=event_time,
        event_location=event_location
    )
    event_cancel_message_body = event_messages.get('cancel', '').format(
        event_title=event_title,
        event_date=event_date,
        event_time=event_time,
        event_location=event_location
    )
    if request_type == "POST":
        try:
            message = client.messages.create(
                to=phone_number,
                from_=twilio_phone_number,
                body=event_create_message_body
            )
            print(f"New Event SMS sent to {phone_number} successfully! SID: {message.sid}")
        except Exception as e:
            print(f"Failed to send New Event SMS to {phone_number}. Error: {str(e)}")
    elif request_type=="PUT":
        try:
            message = client.messages.create(
                to=phone_number,
                from_=twilio_phone_number,
                body=event_update_message_body
            )
            print(f"Event Updated SMS sent to {phone_number} successfully! SID: {message.sid}")
        except Exception as e:
            print(f"Failed to send updated SMS to {phone_number}. Error: {str(e)}")
    elif request_type=="DELETE":
        try:
            message = client.messages.create(
                to=phone_number,
                from_=twilio_phone_number,
                body=event_cancel_message_body
            )
            print(f"Cancellation SMS sent to {phone_number} successfully! SID: {message.sid}")
        except Exception as e:
            print(f"Failed to send cancellation SMS to {phone_number}. Error: {str(e)}")
