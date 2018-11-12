from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import os

@csrf_exempt
# 봇의 메시지를 리턴하는 함수 
def message(request):
	
	json_str = ((request.body).decode('utf-8'))
	received_json = json.loads(json_str) 
	content_name = received_json['content']	

	if content_name == '상품검색':
		return JsonResponse(
		{
			
			'message': {
				'text': '원하는 상품의 이름을 써주세요.'
			},
			'keyboard': {
				'type': 'text' 
			}
		})
	else:
		#Chatbot = chat.chatbot()
		#Chatbot.get_input(content_name)
		#3result = Chatbot.run()
		result = content_name
		
		return JsonResponse(
		{
			'message': {
				'text': result+''
			}
		})



def keyboard(request):

	return JsonResponse(
	{
		'type': 'buttons',
		'buttons': ['상품검색']
	}
	)

