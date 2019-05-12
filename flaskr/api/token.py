from . import api
from flask import request, current_app, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from ..tools import db_tool
 
@api.route('/tokens', methods = ['POST'])
def get_token():
    data = request.get_json()
    email = data.get('email')
    pwd = data.get('pwd')
    with db_tool.get_cursor() as cursor:
        sql = "SELECT id, nm FROM user_info WHERE email = %s AND pwd = %s"
        if cursor.execute(sql, (email, pwd)) == 0:
            return {'message': 'email or pwd is wrong'}
        result = cursor.fetchone()
    s = Serializer(current_app.config['SECRET_KEY'], expires_in = 36000)
    token = s.dumps({'user_id': result['id']}).decode('utf-8')
    return jsonify({
        'id' : result['id'],
        'nm' : result['nm'],
        'token' : token
    })




        