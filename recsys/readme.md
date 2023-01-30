# Recsys
이미지+태그 모델과 이미지 + 카테고리 모델을 concat하여 euclidean distance를 구한 후 가장 유사한 아이템 5개를 추천해줍니다.  <br/>

옷의 형태,색상등 이미지 정보와 옷의 카테고리 (셔츠,치마,트레이닝바지,슬랙스 등) 를 모두 반영한 아이템을 추천합니다. 

## STRUCTURE

├── README.md <br/>
├── final_model<br/>
├── categories  <br/>
│     ├───Preprocess_categories.py<br/>
│     ├───Mobilenet_categories.py<br/>
│     ├───Train_categories.py<br/>
│     └───Embedding_categories.py<br/>
│   ├── show_and_tell<br/>
│     ├───Proprecess.py<br/>
│     ├───Modeling.py<br/>
│     ├───Training.py<br/>
│     └───Embedding.py<br/>
├── similarity <br/>
│     └─── similarity.py<br/>

Preprocess_categories.py : mobilenet 모델에 적용시키기 위한 데이터 전처리 및 dataloader를 만드는 코드입니다.<br/>

Mobilenet_categories.py : mobilenet 모델이 정의된 코드입니다.<br/>

Train_categories: 모델을 학습시키기 위한 코드입니다.<br/>

Embedding_categories.py : 학습된 모델에서 cateogories와 image가 들어가 있는 embedding을 추출하는 코드입니다.<br/>

Proprecess.py : 데이터 전처리 및 kor2vec embedding을 만들고 저장하고 show and tell 모델에 적용시키기 위한 dataloader를 만드는 코드입니다.<br/>

Modeling.py : show and tell 모델이 정의된 코드입니다.<br/>

Training.py : show_and_tell 모델을 학습시키기 위한 코드입니다.<br/>

Embedding.py : 학습된 show_and_tell 모델에서 tag와 image가 들어가있는 embedding을 추출하는 코드입니다.<br/>

similarity.py : show and tell model의 embedding과 categories model의 embedding을 결합하고, 투입된 image와 결합한 embedding 파일의 유사도를 구하여 가장 가까운 5개운 옷를 추천해주는 코드입니다.<br/>

