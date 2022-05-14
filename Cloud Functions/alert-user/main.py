def check_alert(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    from twilio.rest import Client

    request_json = request.get_json()

    # Only alert user if non-normal ECG reading
    if "normal" == request_json['message'].lower():
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Credentials": True,
            },
            "body": "success",
        }

    account_sid = 'TWILIO_ID'
    auth_token = 'TWILIO_AUTH_TOKEN'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body=f"You may be experiencing {request_json['message']}",
            from_='TWILIO_NUMBER',
            to='USER_NUMBER'
        )

    print(message.sid)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Credentials": True,
        },
        "body": "success",
    }
