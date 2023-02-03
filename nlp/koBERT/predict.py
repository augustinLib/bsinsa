import torch
from torch import nn
from torch.utils.data import DataLoader
import gluonnlp as nlp
from tqdm import tqdm
import numpy as np

from .utils import *
from koBERT.loader import koBERTDataset
from koBERT.utils import data_preprocess, calc_accuracy
from koBERT.koBERT_model.model import koBERTClassifier

from kobert_tokenizer import KoBERTTokenizer
from transformers import BertModel
from transformers import AdamW
from transformers.optimization import get_cosine_schedule_with_warmup



def predict(config, text):
    device = torch.device('cpu') if config.gpu_id < 0 else torch.device('cuda:%d' % config.gpu_id)

    tokenizer = KoBERTTokenizer.from_pretrained("skt/kobert-base-v1")
    tok = tokenizer.tokenize
    bertmodel = BertModel.from_pretrained("skt/kobert-base-v1", return_dict=False)
    vocab = nlp.vocab.BERTVocab.from_sentencepiece(
        tokenizer.vocab_file, padding_token="[PAD]"
    )
    print("토크나이저 불러오기")

    model = torch.load("./koBERT/koBERT_model/_batch64_epochs10.pt").to(device)

    predict_data = [[text, 0]]
    predict_dataset = koBERTDataset(predict_data, 0, 1, tok, vocab, config.max_len, True, False)
    predict_dataloader = DataLoader(predict_dataset, batch_size=1, num_workers=5)

    results = []
    for (token_ids, valid_length, segment_ids, label) in predict_dataloader:
        token_ids = token_ids.long().to(device)
        segment_ids = segment_ids.long().to(device)
        valid_length= valid_length
        label = label.long().to(device)
        out = model(token_ids, valid_length, segment_ids)
        for i in out:
            logits=i
            logits = logits.detach().cpu().numpy()
            probability = []
            logits = np.round(new_softmax(logits), 3).tolist()
            temp = np.argmax(logits)
            results.append(temp)

    return results[0]
