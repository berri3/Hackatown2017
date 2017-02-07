#edited 20:26

import http.client, urllib.parse
import json
import pprint
import os
from VoiceDirection import *
from Credentials import *


#-------------------------------------------------------------------------------------------------------

location1 = Location(1, "A", "123")
intercom1 = Intercom(999, location1)


#-------------------------------------------------------------------------------------------------------

def send_message(endpoint, message):
	conn = http.client.HTTPConnection("localhost", 18080)
	conn.request("PUT", endpoint, json.dumps(message).encode('utf-8'))
	response = conn.getresponse()
	data = response.read()
	conn.close()
	if response.status != 200:
		print(response, data)
		return False
	else:
		return True

def get_message():
	conn = http.client.HTTPConnection("localhost", 18080)
	conn.request("GET", "/events")
	response = conn.getresponse()
	data = response.read()
	conn.close()

	if response.status != 200:
		print(response, data)
		return None
	else:
		return json.loads(data.decode('utf-8'))

def get_sound_path(filename):
	# get path to sound files that are in the same directory as the python script
	return os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)


send_message('/configure', {
	"credentials": {
				"app_id": return_app_id(),
				"app_key": return_app_key
			},
			"wakeup": {
				"phrases": [
					'hey dragon',
					'hello dragon',
					'hey raspberry'
				],
				"beep": get_sound_path('listen.pcm'),
			},
			"recognition": {
				"context_tag": "M5168_A2431" 
			},
	})

send_message('/output/file', {'path': get_sound_path('startup.pcm')})

listening = False
while True:
	message = get_message()
	if message is None:
		break
	pprint.pprint(message)

	if message['event'] == 'recognition_state':
		if message['state'] == 'listening_for_speech':
			spoken_text = None
			intent = None
			listening = True
		elif message['state'] == 'processing_speech':
			send_message('/output/file', {'path': get_sound_path('processing.pcm')})
			listening = False

		elif message['state'] == 'waiting_for_wakeup':
			if listening:
				send_message('/output/file', {'path': get_sound_path('timeout.pcm')})
			listening = False

	elif message['event'] == 'recognition_result':
		spoken_text = message.get('transcriptions', [None])[0]
		if spoken_text is not None:
			send_message('/output/synthesize', {'text': 'You said %s' % (spoken_text,)})
		else:
			send_message('/output/file', {'path': get_sound_path('no_utt.pcm')})

	elif message['event'] == 'understanding_result':
		intent = message.get('nlu_interpretation_results',{}).get('payload',{}).get('interpretations',[{}])[0].get('action',{}).get('intent',{}).get('value')
		location = message.get('nlu_interpretation_results',{}).get('payload',{}).get('concepts',{}).get('location',[{}])[0].get('value')
		if intent is not None:
			send_message('/output/synthesize', {'text': 'Your intent is %s' % (intent.lower().replace('_',' '),)})
			send_message('/output/synthesize', {'text': 'You should go %s' % (parse_intent(intent, intercom1),)})
			if intent == 'NO_MATCH':
				send_message('/output/file', {'path': get_sound_path('no_nlu.pcm')})
			else:
				send_message('/output/file', {'path': get_sound_path('success.pcm')})
		else:
			send_message('/output/file', {'path': get_sound_path('no_nlu.pcm')})


