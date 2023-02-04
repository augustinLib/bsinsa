from kobert_tokenizer import KoBERTTokenizer
import gluonnlp as nlp
import pytorch_lightning as pl
from transformers import BertModel
from transformers import AdamW
import numpy as np
from tqdm import tqdm, tqdm_notebook
import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
from transformers import AdamW
from sklearn.model_selection import train_test_split
import pandas as pd
from typing import List,Tuple


class TagDataset(Dataset):
    def __init__(self,df:pd.DataFrame, predict=False):
        
        self.config  = {
                        'EPOCHS':20,
                        'LEARNING_RATE':0.00002,
                        'DROP_RATE' : 0.2,
                        'MAX_LEN' : 100,
                        'SEED':42
                        }
        
        label = ['-','DES','FEEL','FIT','PRIC','PUR']
        self.label_dict = {word:i for i, word in enumerate(label)}
        self.label_dict.update({"[PAD]":len(self.label_dict)})
        self.index_to_ner = {i:j for j, i in self.label_dict.items()}
                           
        self.df = df
        self.predict= predict
        if predict:
            self.tokenizer2 = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
        else:
            self.tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1', sp_model_kwargs={'nbest_size': -1, 'alpha': 0.6, 'enable_sampling': True})

        
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self,index):
        ret = {}
        if self.predict:
            token = self.df['sentences'].values[index]
            tokenized_texts = [self.tokenizing(token)]

            tokenized_text = [token_label_pair[0] for token_label_pair in tokenized_texts] 
            input_ids = [token_label_pair[1][0]['input_ids'] for token_label_pair in tokenized_texts]
            
            token_type_ids = [token_label_pair[1][0]['token_type_ids'] for token_label_pair in tokenized_texts]
            attention_mask = [token_label_pair[1][0]['attention_mask'] for token_label_pair in tokenized_texts]

            ret['input_ids'] = torch.Tensor(input_ids)
            ret['token_type_ids'] = torch.Tensor(token_type_ids)
            ret['attention_mask'] = torch.Tensor(attention_mask)
        else:
            token = self.df['sentences'].values[index]
            labels = self.df['labels'].values[index]

            tokenized_texts_and_labels = [self.tokenize_and_preserve_labels(token, labels)]
            
            tokenized_texts = [token_label_pair[0] for token_label_pair in tokenized_texts_and_labels] 
            input_ids = [token_label_pair[1][0]['input_ids'] for token_label_pair in tokenized_texts_and_labels]
            token_type_ids = [token_label_pair[1][0]['token_type_ids'] for token_label_pair in tokenized_texts_and_labels]
            attention_mask = [token_label_pair[1][0]['attention_mask'] for token_label_pair in tokenized_texts_and_labels]
            labels = [token_label_pair[2] for token_label_pair in tokenized_texts_and_labels]    

            ret['input_ids'] = torch.Tensor(input_ids)
            ret['token_type_ids'] = torch.Tensor(token_type_ids)
            ret['attention_mask'] = torch.Tensor(attention_mask)
            ret['labels'] = torch.Tensor(labels)

        return ret

    def tokenize_and_preserve_labels(self,sentence, text_labels):
        tokenized_sentence = []
        tokenized_dict = []
        labels = []

        for word, label in zip(sentence, text_labels):
            tokenized_word = self.tokenizer.tokenize(word)
            
            n_subwords = len(tokenized_word)

            tokenized_sentence.extend(tokenized_word)
            
            labels.extend([label] * n_subwords)

        tokenized_encode = self.tokenizer.encode_plus(tokenized_sentence,add_special_tokens=False,padding='max_length',truncation=True,max_length=self.config['MAX_LEN'])
        tokenized_dict.append(tokenized_encode)
        diff = self.config['MAX_LEN'] - len(labels)
        if len(labels) > self.config['MAX_LEN']:
            labels = labels[:100]
            labels[-1] = self.label_dict['-']
        else:
            labels.extend([self.label_dict['[PAD]']]*diff)

        return tokenized_sentence,tokenized_dict,labels

    def tokenizing(self,sentences):
        tokenized_sentence = []
        tokenized_dict = []

        sentence = sentences.split(' ')
        tokenized_sentence.append('[CLS]')
        for word in sentence:
            tokenized_word = self.tokenizer2.tokenize(word)
            tokenized_sentence.extend(tokenized_word)

        tokenized_sentence.append('[SEP]')
        tokenized_encode = self.tokenizer2.encode_plus(tokenized_sentence,add_special_tokens=False,padding='max_length',truncation=True,max_length=self.config['MAX_LEN'])
        tokenized_dict.append(tokenized_encode)

        return tokenized_sentence,tokenized_dict
    
    
    
class koBERTDataset(Dataset):
    def __init__(
        self, dataset, sent_idx, label_idx, bert_tokenizer, vocab, max_len, pad, pair
    ):
        transform = nlp.data.BERTSentenceTransform(
            bert_tokenizer, max_seq_length=max_len, vocab=vocab, pad=pad, pair=pair
        )

        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]

    def __getitem__(self, i):
        return self.sentences[i] + (self.labels[i],)

    def __len__(self):
        return len(self.labels)
    

class TagModel(pl.LightningModule):
    def __init__(self, config, train,val,char2idx,idx2char):
        super(TagModel,self).__init__()
        self.config = {
            'EPOCHS':20,
            'LEARNING_RATE':0.00002,
            'BATCH_SIZE':128,
            'DROP_RATE' : 0.2,
            'MAX_LEN' : 100,
            'SEED':42
        }  
        self.kobert = BertModel.from_pretrained('skt/kobert-base-v1')
        self.tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1', sp_model_kwargs={'nbest_size': -1, 'alpha': 0.6, 'enable_sampling': True})
        self.classifier = nn.Linear(768,7)

        self.char2idx = char2idx
        self.idx2char = idx2char

        if config['DROP_RATE'] == 0:
            self.dropout = None
        else:
            self.dropout = nn.Dropout(p=config['DROP_RATE'])
        

    def forward(self, input_ids,token_type_ids, attention_mask):
        outputs = self.kobert(input_ids = input_ids.to(torch.long), token_type_ids = token_type_ids.to(torch.long),attention_mask=attention_mask.float().type_as(input_ids),return_dict=False)

        if self.dropout != None:
            outputs = self.dropout(outputs[0])
        return self.classifier(outputs) # batch,100,7

    def configure_optimizers(self):
        optimizer = AdamW(self.parameters(), lr=self.config['LEARNING_RATE'])
        return optimizer
    '''
    def training_step(self, batch, batch_idx):
        criterion = nn.CrossEntropyLoss()
        input_ids, labels = batch['input_ids'].squeeze(1), batch['labels'].squeeze(1)
        token_type_ids, attention_mask = batch['token_type_ids'].squeeze(1), batch['attention_mask'].squeeze(1)
        
        input_ids = input_ids.to(self.device)
        labels = labels.to(self.device)
        token_type_ids = token_type_ids.to(self.device)
        attention_mask = attention_mask.to(self.device)

        out = self(input_ids,token_type_ids,attention_mask)

        loss = criterion(out.view(-1,out.shape[-1]).to(torch.float),labels.contiguous().view(-1).to(torch.long)) 
        
        return loss

    def validation_step(self, batch, batch_idx):

        criterion = nn.CrossEntropyLoss()
        input_ids, labels = batch['input_ids'].squeeze(1), batch['labels'].squeeze(1)
        token_type_ids, attention_mask = batch['token_type_ids'].squeeze(1), batch['attention_mask'].squeeze(1)
        batch_size = input_ids.size(0)
        
        input_ids = input_ids.to(self.device)
        labels = labels.to(self.device)
        token_type_ids = token_type_ids.to(self.device)
        attention_mask = attention_mask.to(self.device)

        out = self(input_ids,token_type_ids,attention_mask)

        loss = criterion(out.view(-1,out.shape[-1]).to(torch.float),labels.contiguous().view(-1).to(torch.long))       

        _,out = torch.max(out,dim=2)

       
        
        gt = []
        predict = []
        text = []
        for index in range(batch_size):
            pred = [self.idx2char[i.item()] for i in out[index, :]]
            predict.append(pred)
            gt_ = [self.idx2char[i.item()] for i in labels[index,:]]
            gt.append(gt_)
            text_ = self.tokenizer.convert_ids_to_tokens(input_ids[index])
            text.append(text_)
            
        return {'loss':loss,'predict':predict,'ground_truth':gt,'text':text}

    def validation_epoch_end(self,outs):
        count = 0
        loss = []
        pred = []
        gt = []
        text = []
        for dic in outs:
            loss.append(dic['loss'].item())
            pred.extend(dic['predict'])
            gt.extend(dic['ground_truth'])
            text.extend(dic['text'])
        loss = np.mean(loss)

        text = text[:3]
        pred = pred[:3]
        gt = gt[:3]

        for t,p,g in zip(text,pred,gt):
            print(f'text:{t}')
            print(f'pred: {p}')
            print(f'gt: {g}')
            print()
        print(f"loss: {loss}")
        self.log("val_loss",loss)        
            
    '''        
    def predict_step(self, batch, batch_idx):

        input_ids = batch['input_ids'].squeeze(1)
        token_type_ids, attention_mask = batch['token_type_ids'].squeeze(1), batch['attention_mask'].squeeze(1)
        batch_size = input_ids.size(0)

        input_ids = input_ids.to(self.device)
        token_type_ids = token_type_ids.to(self.device)
        attention_mask = attention_mask.to(self.device)

        out = self(input_ids,token_type_ids,attention_mask)

        _,out = torch.max(out,dim=2)

        result = []
        text = []
        outputs = []
        outputs_string = []
        for index in range(batch_size):
            pred = [self.idx2char[i.item()] for i in out[index, :]]
            result.append(pred)
            text_ = self.tokenizer.convert_ids_to_tokens(input_ids[index])
            text.append(text_)


        for i in result:
            outputs.append(i[1:i.index('[PAD]')-1])

        for i in text:
            outputs_string.append(i[1:i.index('[PAD]')-1])


        return outputs_string,outputs


def new_softmax(a):
    c = np.max(a)
    exp_a = np.exp(a - c)
    sum_exp_a = np.sum(exp_a)
    y = (exp_a / sum_exp_a) * 100
    return np.round(y, 3)


class LabelConfig():
    def __init__(self) -> None:
        self.gpu_id = 0
        self.max_len = 64
     
class NLPInference():
    def __init__(self):
        self.label_config = LabelConfig()
        self.tag_config =  {
            'EPOCHS':20,
            'LEARNING_RATE':0.00002,
            'BATCH_SIZE':128,
            'DROP_RATE' : 0.2,
            'MAX_LEN' : 100,
            'SEED':42
        }
        self
        tag_label = ['-','DES','FEEL','FIT','PRIC','PUR']
        self.tag_label_dict = {word:i for i, word in enumerate(tag_label)}
        self.tag_label_dict.update({"[PAD]":len(self.tag_label_dict)})
        self.tag_index_to_ner = {i:j for j, i in self.tag_label_dict.items()}
        
        self.device = torch.device('cpu') if self.label_config.gpu_id < 0 else torch.device('cuda:%d' % self.label_config.gpu_id)
        
        self.label_tokenizer = KoBERTTokenizer.from_pretrained("skt/kobert-base-v1")
        self.tok = self.label_tokenizer.tokenize
        self.label_vocab = nlp.vocab.BERTVocab.from_sentencepiece(
             self.label_tokenizer.vocab_file, padding_token="[PAD]"
        )
        
        self.label_model = torch.load("./nlp_inference/model/_10epochs_batch_64.pt").to(self.device)
        
    
    def label_predict(self, text):
        label_data = [[text, 0]]
        label_dataset = koBERTDataset(label_data, 0, 1, self.tok, self.label_vocab, self.label_config.max_len, True, False)
        label_dataloader = DataLoader(label_dataset, batch_size=1, num_workers=5)

        results = []
        for (token_ids, valid_length, segment_ids, label) in label_dataloader:
            token_ids = token_ids.long().to(self.device)
            segment_ids = segment_ids.long().to(self.device)
            valid_length= valid_length
            label = label.long().to(self.device)
            out = self.label_model(token_ids, valid_length, segment_ids)
            for i in out:
                logits=i
                logits = logits.detach().cpu().numpy()
                probability = []
                logits = np.round(new_softmax(logits), 3).tolist()
                temp = np.argmax(logits)
                results.append(temp)

        return results[0]
        
    
    def tag_predict(self, text):
        data = {
            "idx" : [0],
            "sentences" : [text]
        }

        df = pd.DataFrame(data)
        test_dataset = TagDataset(df, predict=True)
        test_dataloader = DataLoader(test_dataset,batch_size=self.tag_config['BATCH_SIZE'],shuffle=False,num_workers=2)
        model = TagModel(self.tag_config,None,None,self.tag_label_dict,self.tag_index_to_ner)
        trainer = pl.Trainer(accelerator='auto',devices='auto',max_epochs=self.tag_config['EPOCHS'])
        a = trainer.predict(model,test_dataloader,ckpt_path='./nlp_inference/model/kobert_review_classification.ckpt')
        
        result = self._convert(a)
        
        return result
        
        
    def _convert(self, result):
        '''
        List[Tuple[List[List[str]]]]) -> Tuple(List[str],List[List[str]],List[List[int]]):
        return
        output : 토크나이징 되어있는 토큰들을 다시 문장 형태로 만들어서 return 
        output_label : output 각 띄어쓰기 단위에서 classification된 결과
        categori : 해당 문장에서 classification된 카테고리를 1로 표시
        '''
        text = result[0][0]
        label = result[0][1]
        cat = ['DES','FEEL','FIT','PRIC','PUR']

        output = []
        output_label = []
        categori = []
        for i,tex in enumerate(text):
            tmp = []
            output.append(''.join(tex).replace('▁',' ').lstrip())
            for j,word in enumerate(tex):
                if '▁' in word:
                    tmp.append(label[i][j])

            numerical = [0,0,0,0,0]
            for i in range(len(cat)):
                if cat[i] in tmp:
                    numerical[i] = 1
            categori.append(numerical)
            output_label.append(tmp)
            result_list = []
            
            for i in output_label[0]:
                if i == "DES":
                    result_list.append("디자인이 좋아요")
                    
                elif i == "FEEL":
                    result_list.append("감각적이에요")
                    
                elif i == "FIT":
                    result_list.append("정사이즈에요")
                    
                elif i == "PRIC":
                    result_list.append("가격이 착해요")
                    
                elif i == "PUR":
                    result_list.append("특별한 날 입어요")
                    
        return result_list
                    
    def predict(self, text):
        tag_result = self.tag_predict(text)
        label_result = self.label_predict(text)
    
        if label_result == 1:
            label_result = "보통이에요"

        elif label_result == 2:
            label_result = "좋아요"

        else:
            label_result = "별로에요"
            
        new_tag_result = []
        tag_list = set(tag_result)
        for i in tag_list:
            new_tag_result.append(i)
        
        if len(new_tag_result) == 0:
            new_tag_result= ["태그가 없습니다"]
        
        return_dict = {}
        return_dict["tag"] = new_tag_result
        return_dict["label"] = label_result
        
        return return_dict
        




