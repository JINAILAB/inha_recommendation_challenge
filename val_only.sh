# checkpoint file 안에 모든 best ckpt에 대해서 inference 진행 
# inference는 ./src/recommend_topk에 저장됨.

cd ./src
dir_path="./model_ckpt"

for file in "$dir_path"/*.ckpt
do
    echo $file
    python3 main.py -m BM3 -d dacon --val-only --best-ckpt "$file"
done

cd ../predict

## final.csv 생성 
python3 ensemble.py