# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import create_reply
from wechatpy.replies import ArticlesReply
import MySQLdb
import requests
import json

app = Flask(__name__)

@app.route('/wx',methods=['GET','POST'])
def wechat():
        if request.method=='GET':
		token='****'
		data=request.args
            	signature=data.get('signature','')
            	timestamp=data.get('timestamp','')
            	nonce=data.get('nonce','')
            	echostr=data.get('echostr','')
	    	try:
			check_signature(token,signature,timestamp,nonce)
	    	except InvalidSignatureException:
			return ""
	    	return echostr
	else:
		try:
			msg=parse_message(request.data)
		except InvalidSignatureException:
			return ""
		if msg.type=='text':
			retmsg=[{"title": "检索结果","image": "http://*.*.*.*:*/*.jpg", "url": u"http://*.*.*.*:*/*.php?title="+msg.content},]
			reply = ArticlesReply(message=msg, articles=retmsg)
			return reply.render()
		if msg.type=='image':
			image_content='图片.jpg'
			reply=create_reply(image_content,msg)
			return reply.render()
		if msg.type=='voice':
			voice_content='喂喂喂？'
			reply=create_reply(voice_content,msg)
			return reply.render()
		if msg.type=='event':
			welcome_content='欢迎关注我的微信公众号~~ 直接输入关键字可检索有关Github项目'
			reply=create_reply(welcome_content,msg)
			return reply.render()
		else :
			return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
