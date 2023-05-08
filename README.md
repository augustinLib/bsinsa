# ![Title](https://capsule-render.vercel.app/api?type=transparent&fontColor=000000&text=NLP-RecSys%20Based%20Fashion%20E-Commerce%20Demo%20&height=200&fontSize=35&desc=Bitamin%209th%20Conference%202023%20%20&descAlignY=76&descAlign=50)

## Abstract

**NLP Recommendation System Based Fashion E-Commerce Platform Demo** built with Pytorch, Huggingface, React, Express, FastAPI.

<div align="center">
<img src=images/demo1.gif width="574" height="331"/> <br> 
<img src=images/demo2.gif width="574" height="331"/> <br> 
</div>

## Introduction

This GitHub repository contains the source code for our fashion e-commerce website demo, which serves various AI technologies that could be implemented in the web fashion platform. Our website features recommendation systems based on user likes, the ability to find similar items, and review summaries. These AI models are served with FastAPI, while the frontend is built with React and the backend with ExpressJS. We utilized Selenium to gather data such as images and item details, ensuring our AI models are provided with relevant information. The website has an intuitive and user-friendly interface that allows users to easily navigate and find their desired items. <br> <br>

## Data

We extracted 45,000 product information and photos, and 700,000 product review informations using Selenium. For more information, visit [this repository](https://github.com/augustinLib/GitHub-crawling-session). <br> [Data column] Name, Brand, Likes, Sales, Review Score, Price<br><br>

## Recommendation System

Our recommendation system consist of three parts.

- Image + Category Created an image feature (embedding vector) extractor that incorporates category labels using a MobileNet, whose purpose is to speed up the training and inference.
- Image + Tag Created an image feature (embedding vector) extractor that incorporates tags using the Show and Tell model. To process the Korean, which is a agglutinative language, we used skip-gram based embedding.
- Similarity Concatenated the Image + Category and Image + Tag models and calculated Euclidean distance to recommend the 5 most similar items.

<div align="center">
<img src=images/rec_model1.png width="575" height="370"/> 
<p> [Fig. 1] Model Structure </p>
<img src=images/rec_model2.png width="575" height="370"/> 
<p> [Fig. 2] Similarity Result </p>
</div>

## Review Summarization

Our review summarization system consist of two parts.

- Text Review to Score : Using koBERT's cls tokens, we finetuned the model to classify review text of an item to score, 1 to 5.
- Review Keyword Extraction : Using Khaiii tokenizer, seed word, Skip-gram, We finetuned koBERT with 5M sentence with 54 words.

## Web Development

- Frontend : React JS with Typescript
- Backend : Express JS with MongoDB
- AI Model : FastAPI
