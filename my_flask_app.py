# _*_ coding: utf-8 _*_
import os
from flask import Flask, jsonify, request, url_for
from flask import render_template
import requests
import json
import time
import random
import string
import hashlib
app = Flask(__name__, static_url_path='')

APPID = 'wxcef8a2a975f96c9e'
APPSECRET = 'b5b73c59326dc2ce4d8f80051fbb05e7'

ACCESS_TOKEN = ''
JSAPI_TICKET = ''
NONCESTR = ''
TIMESTAMP = None

SIGNATURE_DICT = dict()


# 服务页面
@app.route('/services')
# @app.route('/hello/<name>')
def services():
    return render_template('services.html')


# 业绩工程页面
@app.route('/projects')
# @app.route('/hello/<name>')
def projects():
    return render_template('projects.html')


# 公司风貌页面
@app.route('/about')
# @app.route('/hello/<name>')
def about():
    return render_template('about.html')


# 联系方式页面
@app.route('/contact')
# @app.route('/hello/<name>')
def contact():
    return render_template('contact.html')


# 分享音乐页面
@app.route('/access')
def share():
    return render_template('test.html')


# 分享音乐页面
@app.route('/share')
def share():
    return render_template('test.html')


# 获取access_token
def access_token():
    token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.\
        format(APPID, APPSECRET)
    res = requests.get(token_url)
    status_code = res.status_code
    if status_code == 200:
        res = res.text
        res = json.loads(res)
        token = res.get('access_token', '')
        return token


# 获取jsapi_ticket
def jsapi_ticket():
    token_url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type=jsapi'.format(ACCESS_TOKEN)
    res = requests.get(token_url)
    status_code = res.status_code
    if status_code == 200:
        res = res.text
        res = json.loads(res)
        ticket = res.get('ticket', '')
        return ticket


# 获取随机字符串
def gen_noncestr():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))


# 获取当前时间戳
def get_timestamp():
    return int(time.time())


# 计算签名
def calc_sign(url):
    my_url = 'jsapi_ticket={}&noncestr={}&timestamp={}&url={}'.\
        format(JSAPI_TICKET, NONCESTR, TIMESTAMP, url)
    return hashlib.sha1(my_url.encode('utf-8')).hexdigest()


@app.route('/kkk/')
def ppp(kkk=None):
    uname = request.args.get('from')
    print(uname)
    return render_template('simple.html')


@app.route('/refresh')
def refreshauth(kkk=None):
    refresh_auth()
    return 'OK'


@app.route('/sign/')
def sign():
    uname = request.args.get('urlparam')
    global ACCESS_TOKEN
    global JSAPI_TICKET
    global NONCESTR
    global TIMESTAMP
    NONCESTR = gen_noncestr()
    TIMESTAMP = get_timestamp()
    SIGNATURE_DICT['nonceStr'] = NONCESTR
    SIGNATURE_DICT['appId'] = APPID
    SIGNATURE_DICT['timestamp'] = TIMESTAMP
    SIGNATURE_DICT['url'] = uname
    SIGNATURE_DICT['signature'] = calc_sign(uname)
    print('appId->{}\nsignature->{}\n'.format(APPID, SIGNATURE_DICT['signature']))
    return json.dumps(SIGNATURE_DICT, ensure_ascii=False)


def refresh_auth():
    global ACCESS_TOKEN
    global JSAPI_TICKET
    ACCESS_TOKEN = access_token()
    JSAPI_TICKET = jsapi_ticket()


@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    refresh_auth()
    # url_for('static', filename='MP_verify_o4a7u9WNoaCjb43N.txt')
    app.run(host='0.0.0.0', port=80)
