import re
from nltk.stem import WordNetLemmatizer  # 어간 추출
from nltk.corpus import stopwords  # 불용어 배제
from nltk.tokenize import word_tokenize  # 토큰화 작업에 사용
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


class PreProcessing:
    def __init__(self):
        pass

    def text_pre_processing(input):
        # test
        return ""

    def text_cleaning(self, input, regex):  # input 값 정규식 전처리 ( 구두점 기준 전처리 )
        shortword = re.compile(regex)
        return shortword.sub('', input)

    def lemmatization(self, words):  # 어간 추출 ( 문장에서 토큰화 후 사용 )
        n = WordNetLemmatizer()
        return [n.lemmatize(w, 'v') for w in words]

    def stopword(self, input):  # 불용어 제거
        stop_words = set(stopwords.words('korean'))
        word_tokens = word_tokenize(input)

        result = list()
        for word in word_tokens:
            result.append(word)

        return result

    def padding(self, input):  # 최대 길이 만큼 문장의 길이를 맞추어 주는 함수
        padded = pad_sequences(PreProcessing().encoded(self, input))

        return

    def encoded(self, input):
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts_to(input)
        encoded = tokenizer.texts_to_sequences(input)
        encoded = tokenizer.texts_to_sequences(input)
