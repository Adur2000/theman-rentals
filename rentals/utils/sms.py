import africastalking
from django.conf import settings

africastalking.initialize(
    username=settings.AFRICASTALKING_USERNAME,
    api_key=settings.AFRICASTALKING_API_KEY
)

sms = africastalking.SMS

def send_sms_alert(phone_number, message):
    try:
        response = sms.send(message, [phone_number])
        return response
    except Exception as e:
        print(f"SMS Error: {e}")
        return None