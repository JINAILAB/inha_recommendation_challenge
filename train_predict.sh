# 10개 seed에 대해서 훈련 진행 
cd ./src
mkdir ./model_ckpt
python3 ./main.py -m BM3 -d dacon

cd ../

cp 
mkdir ./predict/recommend


# csv파일 predict 폴더로 이동
cp -r ./src/recommend_topk/*.csv ./predict/recommend
cd ./predict
# ensemble 진행
python3 ensemble.py