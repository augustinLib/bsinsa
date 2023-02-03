STRUCTURE

├── README.md 
├── final_model
├── categories  
│     ├───Preprocess_categories.py
│     ├───Mobilenet_categories.py
│     ├───Train_categories.py
│     └───Embedding_categories.py
│   ├── show_and_tell
│     ├───Proprecess.py
│     ├───Modeling.py
│     ├───Training.py
│     └───Embedding.py
├── similarity 
│     └─── similarity.py

Preprocess_categories.py : mobilenet 모델에 적용시키기 위한 데이터 전처리 및 dataloader를 만드는 코드입니다.

Mobilenet_categories.py : mobilenet 모델이 정의된 코드입니다.

Train_categories: 모델을 학습시키기 위한 코드입니다.

Embedding_categories.py : 학습된 모델에서 cateogories와 image가 들어가 있는 embedding을 추출하는 코드입니다.

Proprecess.py : 데이터 전처리 및 kor2vec embedding을 만들고 저장하고 show and tell 모델에 적용시키기 위한 dataloader를 만드는 코드입니다.

Modeling.py : show and tell 모델이 정의된 코드입니다.

Training.py : show_and_tell 모델을 학습시키기 위한 코드입니다.

Embedding.py : 학습된 show_and_tell 모델에서 tag와 image가 들어가있는 embedding을 추출하는 코드입니다.

similarity.py : show and tell model의 embedding과 categories model의 embedding을 결합하고, 투입된 image와 결합한 embedding 파일의 유사도를 구하여 가장 가까운 5개운 옷를 추천해주는 코드입니다.
