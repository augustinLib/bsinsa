import torch
from torch import nn
from torch.utils.data import DataLoader
import gluonnlp as nlp
from tqdm import tqdm
from sklearn.model_selection import train_test_split

from koBERT.loader import koBERTDataset
from koBERT.utils import data_preprocess, calc_accuracy
from koBERT.koBERT_model.model import koBERTClassifier

from kobert_tokenizer import KoBERTTokenizer
from transformers import BertModel
from transformers import AdamW
from transformers.optimization import get_cosine_schedule_with_warmup


def train(config):
    device = (
        torch.device("cpu")
        if config.gpu_id < 0
        else torch.device("cuda:%d" % config.gpu_id)
    )

    tokenizer = KoBERTTokenizer.from_pretrained("skt/kobert-base-v1")
    tok = tokenizer.tokenize
    bertmodel = BertModel.from_pretrained("skt/kobert-base-v1", return_dict=False)
    vocab = nlp.vocab.BERTVocab.from_sentencepiece(
        tokenizer.vocab_file, padding_token="[PAD]"
    )

    train_data = data_preprocess("./train.csv")
    valid_data = data_preprocess("./valid.csv")

    train_dataset = koBERTDataset(
        train_data, 0, 1, tok, vocab, config.max_len, True, False
    )
    valid_dataset = koBERTDataset(
        valid_data, 0, 1, tok, vocab, config.max_len, True, False
    )

    train_dataloader = DataLoader(
        train_dataset, batch_size=config.batch_size, num_workers=5
    )
    valid_dataloader = DataLoader(
        valid_dataset, batch_size=config.batch_size, num_workers=5
    )

    model = koBERTClassifier(bertmodel, dr_rate=config.dropout_p).to(device)

    no_decay = ["bias", "LayerNorm.weight"]
    optimizer_grouped_parameters = [
        {
            "params": [
                p
                for n, p in model.named_parameters()
                if not any(nd in n for nd in no_decay)
            ],
            "weight_decay": 0.01,
        },
        {
            "params": [
                p
                for n, p in model.named_parameters()
                if any(nd in n for nd in no_decay)
            ],
            "weight_decay": 0.0,
        },
    ]

    optimizer = AdamW(optimizer_grouped_parameters, lr=config.learning_rate)
    loss_fn = nn.CrossEntropyLoss()
    t_total = len(train_dataloader) * config.num_epochs
    warmup_step = int(t_total * config.warmup_ratio)
    scheduler = get_cosine_schedule_with_warmup(
        optimizer, num_warmup_steps=warmup_step, num_training_steps=t_total
    )

    for e in range(config.num_epochs):
        train_acc = 0.0
        test_acc = 0.0
        model.train()
        for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(
            tqdm(train_dataloader)
        ):
            optimizer.zero_grad()
            token_ids = token_ids.long().to(device)
            segment_ids = segment_ids.long().to(device)
            valid_length = valid_length
            label = label.long().to(device)
            out = model(token_ids, valid_length, segment_ids)
            loss = loss_fn(out, label)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), config.max_grad_norm)
            optimizer.step()
            scheduler.step()  # Update learning rate schedule
            train_acc += calc_accuracy(out, label)
            # if batch_id % config.log_interval == 0:
            #     print("epoch {} batch id {} loss {} train acc {}".format(e+1, batch_id+1, loss.data.cpu().numpy(), train_acc / (batch_id+1)))
        print("epoch {} train acc {}".format(e + 1, train_acc / (batch_id + 1)))
        model.eval()
        for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(
            tqdm(valid_dataloader)
        ):
            token_ids = token_ids.long().to(device)
            segment_ids = segment_ids.long().to(device)
            valid_length = valid_length
            label = label.long().to(device)
            out = model(token_ids, valid_length, segment_ids)
            test_acc += calc_accuracy(out, label)
        print("epoch {} valid acc {}".format(e + 1, test_acc / (batch_id + 1)))

    PATH = "./koBERT/koBERT_model/"
    torch.save(model, PATH + "_" + config.model_name + ".pt")
    torch.save(model.state_dict(), PATH + "_" + config.model_name + "_state_dict.pt")
    torch.save(
        {"model": model.state_dict(), "optimizer": optimizer.state_dict()},
        PATH + "_" + config.model_name + "all.tar",
    )