from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import os
import logging
from django.views.decorators.http import require_GET

logger = logging.getLogger(__name__)

API_TOKEN = "sk-proj-aLQKAmI7OLSrxRCuwzoiT3BlbkFJwu89UzCKrVzyhLqzBwJT"
API_URL = "https://api.openai.com/v1/audio/transcriptions"

transcription_cache = None  # Cache to store the last transcription

@csrf_exempt
def convert_api(request):
    global transcription_cache
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']

        temp_dir = os.path.join(os.getcwd(), 'temp')
        os.makedirs(temp_dir, exist_ok=True)

        audio_file_path = os.path.join(temp_dir, audio_file.name)

        with open(audio_file_path, 'wb+') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

        try:
            # Leer el archivo de audio
            with open(audio_file_path, 'rb') as f:
                audio_content = f.read()

            # Preparar la solicitud a la API de Whisper
            headers = {
                'Authorization': f'Bearer {API_TOKEN}',
            }
            files = {
                'file': (audio_file.name, audio_content, 'audio/wav'),
                'model': (None, 'whisper-1')  # Añadir el modelo requerido
            }
            response = requests.post(API_URL, headers=headers, files=files)

            if response.status_code == 200:
                result = response.json()
                text = result.get('text', '')
                transcription_cache = text  # Cache the transcription
                os.remove(audio_file_path)
                return JsonResponse({'status': 'success', 'message': 'Audio processed', 'text': text})
            else:
                logger.error("Error processing audio file: %s", response.text)
                os.remove(audio_file_path)
                return JsonResponse({'status': 'error', 'message': 'Failed to process audio'}, status=500)
        except Exception as e:
            if os.path.exists(audio_file_path):
                os.remove(audio_file_path)
            logger.error("Error processing audio file: %s", e, exc_info=True)
            return JsonResponse({'status': 'error', 'message': 'Failed to process audio'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@require_GET
def get_last_transcription(request):
    global transcription_cache
    if transcription_cache:
        return JsonResponse({'status': 'success', 'text': transcription_cache})
    else:
        return JsonResponse({'status': 'error', 'message': 'No transcription available'}, status=404)
