# inha_recommendation_challenge

## 대회 설명

---

### **2023 인하 인공지능 챌린지**

**[주제]**

- 멀티모달 데이터 기반 추천 시스템 (Multi-modal Recommender System)

**[대회설명]**

- 추천 시스템은 사용자의 정보를 분석하여 사용자에게 적합한 상품을 추천해주는 인공지능 기술 중 하나입니다.

추천 시스템 기술을 통해 사용자 편의성 증가 및 사용자의 상품의 접근성을 높여 기업의 이익 증대를 기대 할 수 있습니다.

링크 : [https://dacon.io/competitions/official/236113/overview/description](https://dacon.io/competitions/official/236113/overview/description)

## 모델

---

- **multimodal model** **BM3 (WWW'23) 이용**
    - https://github.com/enoche/BM3
- 빠른 infrence를 위해서 90 epoch 이전 training에 대해서 validate을 진행하지 않았습니다.
- 140epoch에서 훈련을 종료했고 10epoch 이상 validate값이 증가하지 않을 경우 early stopping을 적용했습니다.

### ensemble
- 총 40개의 seed에 대해서 ensemble
- 각각 50개의 최고점수로 sort후 병합 후 다시 최고 점수로 50개 뽑아냅니다.
- seed : [111, 222, 333, 444, 555, 666, 777, 888, 999, 11, 22, 33, 44, ...]
- hyper parameter(find by Grid search)
    - n_layers : [1, **2**]
    - dropout : [**0.3**, 0.5]
    - reg_weight: [0.1, **0.01**]
    

## 실행 방법

---

위에서부터 아래로 실행시키면 predict 폴더에 제출파일(final.csv)이 생깁니다. 

## installation
- docker에서 진행해서 version이 안 맞을 수도 있습니다.
---

```bash
pip install -r requirements.txt
```

## data prepare
- dacon google drive에서 데이터 다운 후 data preprocess를 진행합니다.
---

```bash
sh prepare_data.sh
```

## train & predict (not recommended)

---
총 40개의 model에 대해서 ensemble을 하였습니다.(3-4일 소요)
ensemble하는 수를 줄이고 싶다면 ./src/configs/overall.yaml 파일을 수정해주세요.

```bash
sh train_predict.sh
```

## val-only

---
model_ckpt를 다운 후 inference 후 ensemble

```bash
sh val_only.sh
```