'''
FastText Train Module
'''
import csv
from gensim.models import FastText
from modules.recommender.fasttext.decorators import * 

class Trainer:
    '''FastText Trainer Class'''
    def __init__(self):
        # Hyperparameter
        self.VEC_SIZE = 30
        self.WINDOWS = 10
        self.MIN_COUNT = 10
        self.ITERATION = 1000
        self.WORKERS = 4
        
        self.model = None
        self.corpora = []

    def load_model(self, path):
        '''모델 불러오기'''
        self.model = FastText.load(path)

    @model_require
    def save_model(self, path):
        '''모델 저장하기'''
        self.model.save(path)

    def set_params(
        self,
        vec_size=None,
        windows=None,
        min_count=None,
        iteration=None,
        workers=None
    ):
        '''하이퍼파라미터 세팅'''
        if vec_size and isinstance(vec_size, int):
            self.VEC_SIZE = vec_size
        if windows and isinstance(windows, int):
            self.WINDOWS = windows
        if min_count and isinstance(min_count, int):
            self.MIN_COUNT = min_count
        if iteration and isinstance(iteration, int):
            self.ITERATION = iteration
        if workers and isinstance(workers, int):
            self.WORKERS = workers

    def get_params(self):
        '''하이퍼파라미터 반환'''
        return {
            "workers":self.VEC_SIZE,
            "windows":self.WINDOWS,
            "min_count":self.MIN_COUNT,
            "iteration":self.ITERATION,
            "workers":self.WORKERS
        }
        
    def set_corpora(self, corpora):
        '''학습 코포라 세팅'''
        self.corpora = corpora

    def get_corpora(self):
        '''학습 코포라 반환'''
        return self.corpora

    @timer
    @train_deco
    def train(self):
        '''학습 메소드'''
        self.model = FastText(
            size=self.VEC_SIZE,
            window=self.WINDOWS,
            min_count=self.MIN_COUNT,
            iter=self.ITERATION,
            workers=self.WORKERS,
            sentences=self.corpora)

    @model_require
    @timer
    @update_deco
    def update(self):
        '''전이학습 메소드'''
        self.model.build_vocab(self.corpora, update=True)
        self.model.train(
            self.corpora,
            total_examples=self.model.corpus_count,
            epochs=self.model.epochs)

    @model_require
    def is_in_dict(self, word):
        '''입력된 토큰이 모델이 알고 있는 토큰인지 반환'''
        return word in self.model.wv.vocab

    @model_require
    def export_tsv (self, vec_path = "./vec.tsv", meta_path = "./meta.tsv"):
        '''
        모델 정보를 TSV 포맷으로 추출
        # https://projector.tensorflow.org/ 시각화 전용
        # 파라미터: 벡터 파일 경로, 메타데이터 저장 경로
        '''
        with open(vec_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='\t')
            words = self.model.wv.vocab.keys()
            for word in words:
                row = self.model.wv.get_vector(word).tolist()
                writer.writerow(row)
        with open(meta_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='\t')
            for word in words:writer.writerow([word])

    @model_require
    def export_test_docs(self, words, path = "./모델테스트.md"):
        '''특정 키워드에 대한 모델 성능 측정 및 MD 문서화'''
        with open(path,"w",encoding='utf-8') as f:
            f.write("# 모델 단어 테스트\n\n")
            for ex in words:
                if ex == "": continue
                if not self.is_in_dict(ex): continue
                f.write("### " + str(ex) + " \n")
                f.write(" **" + str(self.sim_words(ex)) + "** \n")
                f.write("\n")