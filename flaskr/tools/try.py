from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

salt = 'dev'
exp_time = 600

def get_token(email, pwd):
    s = Serializer(salt, expires_in = exp_time)
    token = s.dumps({'email': email, 'pwd' : pwd}).decode('utf-8')
    return token

def verify_token(token):
    s = Serializer(salt)
    try:
        data = s.loads(token)
    except:
        return None
    return data


token = get_token('a@me', '123')
print(token)
print(verify_token(token))

