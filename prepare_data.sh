# download data from google drive
gdown https://drive.google.com/uc?id=1Qi5SI-bEDxHmKN_lPaN41MC_oI1TyScw -O ./data/raw_data.zip

# make directory 
mkdir ./data/raw_data ./data/dacon ./src/log ./src/recommend_topk
unzip -qq ./data/raw_data.zip -d ./data/raw_data

# data preprocess for train
python3 ./data/preprocess_data.py
mv ./data/raw_data/data/image.npy ./data/dacon/image_feat.npy
mv ./data/raw_data/data/text.npy ./data/dacon/text_feat.npy
rm -r ./data/raw_data ./data/raw_data.zip

# 제출을 위해서 predict폴더로 복사
cp ./data/dacon/u_id_mapping.csv ./predict
cp ./data/dacon/i_id_mapping.csv ./predict