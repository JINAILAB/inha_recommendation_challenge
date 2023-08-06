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
- 총 9개의 seed에 대해서 ensemble(hard voting)
- seed : [111, 222, 333, 444, 555, 666, 777, 888, 999]
- hyper parameter(find by Grid search)
    - n_layers : [1, **2**]
    - dropout : [**0.3**, 0.5]
    - reg_weight: [0.1, **0.01**]
    

## 실행 방법

---

위에서부터 아래로 실행시키면 predict 폴더에 제출파일(final.csv)이 생깁니다. 

## installation

---

```bash
pip install -r requirements.txt
```

## data prepare

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