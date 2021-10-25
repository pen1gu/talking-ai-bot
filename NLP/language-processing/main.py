from nltk import sent_tokenize, word_tokenize
from konlpy.tag import Hannanum as hnm
from hanspell import spell_checker
from pykospacing import Spacing
import urllib.request
from soynlp import DoublespaceLineCorpus
from soynlp.word import WordExtractor
from konlpy.tag import Okt

def tokenize_text(input): # 단어 토큰화
    sentences = sent_tokenize(text=input)
    word_tokens = [word_tokenize(sentence) for sentence in sentences]
    return word_tokens


def spell_check(input): # 문장 체크
    spelled_sent = spell_checker.check(input)
    hanspell_sent = spelled_sent.checked
    return hanspell_sent

if __name__ == '__main__':
    print(spell_check("안늉하세요"))