def send_sms_alert(phone_number, message):
    """
    Mock SMS alert function for local testing.

    Args:
        phone_number (str): The recipient's phone number.
        message (str): The message content.

    Returns:
        dict: Simulated response.
    """
    print(f"[SMS MOCK] Would send to {phone_number}: {message}")
    return {"status": "mocked", "phone_number": phone_number, "message": message}