import requests
import pygame
import pyaudio
import speech_recognition as sr
import clova_voice

# GPT API URL
gpt_url = "https://api.openai.com/v1/engines/davinci-codex/completions"

# GPT API 토큰
gpt_token = "YOUR_OPENAI_API_KEY"

# 클로바 보이스 API 키
clova_voice_key = "YOUR_CLOVA_VOICE_API_KEY"

# 음성 인식기 객체 생성
recognizer = sr.Recognizer()

# 오디오 출력 초기화
pygame.mixer.init()

# 마이크 설정
microphone = sr.Microphone()

# 음성 인식 함수
def recognize_speech():
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        return recognizer.recognize_google(audio, language='en-US,ja-JP,ko-KR')

# Clova Voice API를 사용하여 음성 출력 함수
def speak(message):
    url = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-NCP-APIGW-API-KEY-ID": "YOUR_NAVER_CLOUD_API_KEY_ID",
        "X-NCP-APIGW-API-KEY": clova_voice_key,
    }
    data = f"speaker=nara&speed=0&text={message}"
    response = requests.post(url, headers=headers, data=data)
    sound = pygame.mixer.Sound(file=pygame.sndarray.make_sound(response.content))
    sound.play()

# GPT API를 사용하여 대화 생성 함수
def generate_response(text):
    prompt = f"I say: {text}\nAI says:"
    data = {
        "prompt": prompt,
        "max_tokens": 60,
        "temperature": 0.7,
        "n": 1,
        "stop": "\n",
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {gpt_token}",
    }
    response = requests.post(gpt_url, json=data, headers=headers)
    return response.json()["choices"][0]["text"]

# 대화 시작
speak("안녕하세요, 무엇을 도와드릴까요?")

while True:
    try:
        # 사용자 음성 인식
        message = recognize_speech()
        print("사용자: ", message)

        # 사용자 입력이 없을 경우
        if not message:
            speak("죄송합니다. 다시 말씀해주세요.")
            continue

        # AI 응답 생성
        response = generate_response(message)
        print("AI: ", response)

        # AI 응답 출력
        speak(response)

    except sr.UnknownValueError:
        speak("죄송합니다. 다시 말씀해주세요.")
    except sr.RequestError:
        speak("죄송합니다. 인터넷 연결을 확인해주세요.")
