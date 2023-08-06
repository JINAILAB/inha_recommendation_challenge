import glob
import pandas as pd
import numpy as np
from collections import Counter
import numpy as np
from tqdm import tqdm

tqdm.pandas()

# 폴더 안에 파일명을 기준으로 seed값 기준 최고성능 뽑기
def check_the_best_file(listdir):
    seed_dict = {}

    for filename in listdir:
        # Split filename by '-'
        parts = filename.split('-')
        
        # Extract seed and index
        seed = parts[1]
        idx = int(parts[3].replace("idx", ""))
        
        # seed가 dict에 없다면 추가
        if seed not in seed_dict:
            seed_dict[seed] = []
        
        # seed에 대해서 index 추가
        seed_dict[seed].append(idx)

    # 출력 파일 리스트
    last_files = []

    # seed에 대해서 반복
    for seed, indices in seed_dict.items():
        # indeices 기준 sort
        indices.sort()
        
        # 가장 큰 마지막 값 가져오기
        last_index = indices[-1]
        
        for filename in listdir:
            if filename.split('-')[1] == seed and int(filename.split('-')[3].replace("idx", "")) == last_index:
                last_files.append(filename)
                break
            
    return last_files




# csv파일을 원래 형태로 변환, id와 scorer 기준으로 정렬
def melt_by_submitform(df, u_map_dict, i_map_dict):
    top_cols = [col for col in df.columns if 'top' in col]
    score_cols = [col for col in df.columns if 'score' in col]

    # top 기준으로 melt
    df_top = df.melt(id_vars='id', value_vars=top_cols, var_name='top_id', value_name='top')

    # score 기준으로 melt
    df_score = df.melt(id_vars='id', value_vars=score_cols, var_name='score_id', value_name='score')

    # 값 확인 
    df_top['top_id'] = df_top['top_id'].str.extract('(\d+)').astype(int)
    df_score['score_id'] = df_score['score_id'].str.extract('(\d+)').astype(int)

    # 두개 데이터 합치기 
    df_melted = pd.merge(df_top, df_score, left_on=['id', 'top_id'], right_on=['id', 'score_id'])
    df_melted.drop(['top_id', 'score_id'], axis=1, inplace=True)
    
    # column rename
    df_melted.rename(columns = {'id':'user_id', 'top':'item_id'}, inplace=True)
    
    # map_csv파일을 이용해서 원래 id로 돌려주기
    df_melted['user_id'] = df_melted['user_id'].map(u_map_dict)
    df_melted['item_id'] = df_melted['item_id'].map(i_map_dict)
    # user_id, score기준으로 sort
    df_melted.sort_values(['user_id', 'score'], ascending=False)
    
    return df_melted


# train.csv에 있는 파일들은 삭제
def delete_name_on_train_csv(final_data, data):
    return final_data[~final_data.set_index(['user_id','item_id']).index.isin(data.set_index(['user_id','item_id']).index)]
    

    
# 모든 데이터들에 대해서 점수 기준 상위 50개 출력    
def ensemble_dfs(combined_df):
    combined_df_sorted = combined_df.sort_values(by=['user_id', 'score'], ascending=False)
    combined_df_grouped = combined_df_sorted.groupby('user_id').progress_apply(lambda x: x.sort_values('score', ascending=False)[:50])

    # resetindex & drop score column
    combined_df_grouped.reset_index(drop=True, inplace=True)
    combined_df_grouped.drop('score', axis=1,inplace=True)
    
    return combined_df_grouped
    

    
    
    

def main():
    item_map = pd.read_csv('i_id_mapping.csv', sep = '\t')
    user_map = pd.read_csv('u_id_mapping.csv', sep = '\t')
    train_csv = pd.read_csv('train.csv')

    i_map_dict = dict(zip(item_map['itemID'], item_map['asin']))
    u_map_dict = dict(zip(user_map['userID'], user_map['user_id']))


    files = glob.glob('./recommend/*.csv')


    best_files = check_the_best_file(files)

    print(f"{len(best_files)} files was selected out of {len(files)} files. let's start ensemble")

    df_list = []

    # file 안에 있는 csv파일 list에 load
    for file in tqdm(best_files):
        df = pd.read_csv(file, sep= '\t')
        df = melt_by_submitform(df, u_map_dict, i_map_dict)
        df = delete_name_on_train_csv(df, train_csv)
        df_list.append(df)
        

    # ensemble을 위해서 전체 데이터 concat
    combined_df = pd.concat(df_list)
    
    # ensemble!!
    ensemble_df = ensemble_dfs(combined_df)
    # 최종 파일 출력
    ensemble_df.to_csv('./final.csv', index=False)
        
        
        
        
if __name__ == "__main__":
    main()
