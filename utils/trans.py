# necessary packages in colab
# !pip install -q sentence_transformers
# !pip install -q mtranslate

from sentence_transformers import SentenceTransformer
from mtranslate import translate
from tqdm import tqdm
import torch


class MultiLangSimilarity():
    def __init__(self, model_name, device='cpu'):
        self.model = SentenceTransformer(model_name, device=device)

    def __call__(self, text):
        return self.model.encode(text,  
                                convert_to_tensor=True,
                                normalize_embeddings=True)

    def score(self, a, b):
        a, b = self([a, b])
        return torch.dot(a, b).item()


class Translator():
    def __init__(self, model_name:str, min_score:float=.9, device:str='cpu'):
        self.min_score = min_score
        self.similar = MultiLangSimilarity(model_name=model_name, device=device)

    def __call__(self, sentences:list):
        outputs = []
        for i, sentence in tqdm(enumerate(sentences), total=len(sentences)):
            aug = translate(sentence, from_language='en', to_language='fa')
            score = self.similar.score(sentence, aug)
            if score >= self.min_score:
                outputs.append({'id': i, 'en': sentence, 'fa': aug, '%': score})
        return outputs


if __name__ == '__main__':
    model_name = 'paraphrase-multilingual-mpnet-base-v2'
    translator = Translator(model_name=model_name, min_score=0.85, device='cpu')
    out = translator(sentences=['would you like something to eat?'])
    print(out)