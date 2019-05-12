from flask import current_app, g, abort, request

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def verify_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        print("token %s" % token)
        data = s.loads(token)
        print(data)
        g.user_id = data['user_id']
    except:
        abort(401)
    return data['user_id']

def get_request_token():
    cookies = request.cookies
    token = cookies.get("token")
    return token


def date_string(date):
    date_str = date.strftime('%Y-%m-%d')
    return date_str





