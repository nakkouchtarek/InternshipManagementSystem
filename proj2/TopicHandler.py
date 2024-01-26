from gensim import corpora
from gensim.models import LdaModel
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class TopicHandler:
    def __init__(self):
        # stop words represent words that are useless in our tretements in order to get rid of them
        self.stop_words = set(stopwords.words('english'))
        # lemmatizing means getting rid of the extra letters in a name but keep the meaning walking, walked, walks -> walk
        self.lemmatizer = WordNetLemmatizer()

    def preprocess_text(self, text):
        # we tokenize the text returning a list of words considering the delimiter is a space
        tokens = word_tokenize(text)
        # now we lemmitize each word
        tokens = [self.lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalpha() and token.lower() not in self.stop_words]
        return tokens
    
    def predict_topic(self, text):
        tokenized_text = self.preprocess_text(text)

        # corpora dictionary maps each word to an id
        dictionary = corpora.Dictionary([tokenized_text])
        # we will count the occurences of each word
        corpus = [dictionary.doc2bow(tokenized_text)]

        # we assume that we have a mix of topics, assign each to a random word,
        # we keep on refining based on the likelihood of words sharing the same topic
        lda_model = LdaModel(corpus, num_topics=1, id2word=dictionary)

        # we extract most probable topics, it will return a list of tuples
        main_topic_representation = lda_model.print_topics()[0][1]

        # we extract those topics
        word_list = [word.split('*')[1].strip().replace('"', '') for word in main_topic_representation.split('+')]

        return ' '.join([word.capitalize() for word in word_list[:2]])