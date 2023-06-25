import nltk
from nltk.tokenize import word_tokenize
from gensim import corpora
from gensim.models import LdaModel
import cv2
import datetime
from config import config
import random
import os
import binascii
import hashlib

stop_words = [
    'и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то', 'все', 'она',
    'так', 'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только', 'ее',
    'мне', 'было', 'вот', 'от', 'меня', 'еще', 'о', 'из', 'ему', 'теперь', 'когда', 'даже',
    'ну', 'вдруг', 'ли', 'если', 'уже', 'или', 'ни', 'быть', 'был', 'него', 'до', 'вас',
    'нибудь', 'опять', 'уж', 'вам', 'ведь', 'там', 'потом', 'себя', 'ничего', 'ей', 'может',
    'они', 'тут', 'где', 'есть', 'надо', 'ней', 'для', 'мы', 'тебя', 'их', 'чем', 'была',
    'сам', 'чтоб', 'без', 'будто', 'чего', 'раз', 'тоже', 'себе', 'под', 'будет', 'ж',
    'тогда', 'кто', 'этот', 'того', 'потому', 'этого', 'какой', 'совсем', 'ним', 'здесь',
    'этом', 'один', 'почти', 'мой', 'тем', 'чтобы', 'нее', 'сейчас', 'были', 'куда',
    'зачем', 'всех', 'никогда', 'можно', 'при', 'наконец', 'два', 'об', 'другой', 'хоть',
    'после', 'над', 'больше', 'тот', 'через', 'эти', 'нас', 'про', 'всего', 'них', 'какая',
    'много', 'разве', 'три', 'эту', 'моя', 'впрочем', 'хорошо', 'свою', 'этой', 'перед',
    'иногда', 'лучше', 'чуть', 'том', 'нельзя', 'такой', 'им', 'более', 'всегда', 'конечно',
    'всю', 'между', ',', '!', '.', ':', ';'
]

class TextAnalyze():

    def __init__(self):
        nltk.download('punkt')
        self.tokenizer = nltk.data.load('tokenizers/punkt/russian.pickle')

    def tokenize_sentences(self, text):
        sentences = self.tokenizer.tokenize(text)
        return sentences

    def tokenize_words(self, sentence):
        words = word_tokenize(sentence)
        return words

    def create_dictionary(self, tokenized_sentences):
        dictionary = corpora.Dictionary(tokenized_sentences)
        return dictionary

    def create_corpus(self, tokenized_sentences, dictionary):
        corpus = [dictionary.doc2bow(tokens) for tokens in tokenized_sentences]
        return corpus

    def get_timestamps(self, transcript):
        timestamps = ["%.2f" % ts['time'] for ts in transcript['segments']]
        return  timestamps

    def capture_frames(self, video_path, timestamps):
        # Открыть видеофайл
        video = cv2.VideoCapture(video_path)

        # Получить частоту кадров (FPS) видео
        fps = video.get(cv2.CAP_PROP_FPS)

        # Создать массив для хранения скриншотов
        frames = []

        # Обработать каждый таймкод
        for timestamp in timestamps:
            # Вычислить номер кадра на основе таймкода и FPS
            timestamp = float(timestamp)
            frame_number = int(timestamp * fps)

            # Установить позицию видеофайла на нужный кадр
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

            # Считать текущий кадр
            ret, frame = video.read()

            # Проверить, удалось ли считать кадр
            if ret:
                # Добавить кадр в массив
                frames.append(frame)

        # Закрыть видеофайл
        video.release()

        return frames
    
    def get_timestamps_for_frames(self, episodes, num_of_frames = 3):
        dur = [ep['end_time'] - ep['start_time'] for ep in episodes]
        stm_per = [int(d/num_of_frames) for d in dur]
        tmstps_ep = []
        tms = []
        j = 0
        for ep in episodes:
            for i in range(0, num_of_frames):
                tmstps_ep.append(ep['start_time'] + stm_per[j] * i)
            tms.append(tmstps_ep)
            tmstps_ep = []
            j += 1
        return tms
    
    def get_segmented_text(self, transcript, episodes, num_of_frames):
        index = 0
        segmented_text = []
        current_episode = episodes[index]
        tms =  self.get_timestamps_for_frames(episodes, num_of_frames)

        paragraph_sentences = []
        for segment in transcript:
            if int(segment['time']) < int(current_episode['end_time']):
                # if len(current_paragraph) == 1:
                paragraph_sentences.append(segment['text'])
            else:
                segmented_text.append({"header": current_episode['title'], "text": paragraph_sentences, "time": current_episode['start_time'], "frames": tms[index] })
                index += 1
                current_episode = episodes[index]
                paragraph_sentences = []
                paragraph_sentences.append(segment['text'])

        if len(paragraph_sentences) != 0:
            segmented_text.append({"header": current_episode['title'], "text": paragraph_sentences, "time": current_episode['start_time'], "frames": tms[index] })

        return segmented_text
    
    def analyze_episodes(self, video_path, transcript, episodes, num_of_frames = 3):
        res = []
        data = self.get_segmented_text(transcript['segments'], episodes, num_of_frames)
        for it in data:
            screenshots = self.capture_frames(video_path, it['frames'])

            list_scr = []
            # Сохранить скриншоты
            for i, screenshot in enumerate(screenshots):
                filename = str(hashlib.md5(os.urandom(32)).hexdigest()) + ".jpg"
                cv2.imwrite(f"{config.picture_storage_path}/{filename}", screenshot)
                list_scr.append(filename)

    
            res.append({
                "type": "header",
                "data": {
                    "text": "[" + str(datetime.timedelta(seconds=int(it["time"]))) + "] " + it["header"],
                }
            })

            for seg in it['text']:
                res.append(
                    {
                        "type": "paragraph",
                        "data": {
                            "text": seg,
                        }
                    }
                )

            for scr in list_scr:
                res.append(
                    {
                        "type" : "image",
                        "data":{
                            "file": {
                                "url" : "http://185.112.83.36:8080/images/" + scr
                            },
                        }
                    }
                )

        return res