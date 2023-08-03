import os
import pandas as pd
import numpy as np
from collections import Counter
import numpy as np
from tqdm import tqdm

tqdm.pandas()
def get_illegal_ids_by_inter_num(df, field, max_num=None, min_num=None):
    if field is None:
        return set()
    if max_num is None and min_num is None:
        return set()

    max_num = max_num or np.inf
    min_num = min_num or -1

    ids = df[field].values
    inter_num = Counter(ids)
    ids = {id_ for id_ in inter_num if inter_num[id_] < min_num or inter_num[id_] > max_num}
    print(f'{len(ids)} illegal_ids_by_inter_num, field={field}')

    return ids


def filter_by_k_core(df):
    while True:
        ban_users = get_illegal_ids_by_inter_num(df, field=learner_id, max_num=None, min_num=min_u_num)
        ban_items = get_illegal_ids_by_inter_num(df, field=course_id, max_num=None, min_num=min_i_num)
        if len(ban_users) == 0 and len(ban_items) == 0:
            return

        dropped_inter = pd.Series(False, index=df.index)
        if learner_id:
            dropped_inter |= df[learner_id].isin(ban_users)
        if course_id:
            dropped_inter |= df[course_id].isin(ban_items)
        print(f'{len(dropped_inter)} dropped interactions')
        df.drop(df.index[dropped_inter], inplace=True)


# data shuffle and train valid test로 나누기
def split_data(df):
    df = df.sample(frac=1)  # Shuffle the data
    cutoff_l = int(len(df) * 0.8)
    cutoff_u = int(len(df) * 0.9)
    
    df.iloc[:cutoff_l, df.columns.get_loc('split')] = 'train'
    df.iloc[cutoff_l:cutoff_u, df.columns.get_loc('split')] = 'valid'
    df.iloc[cutoff_u:, df.columns.get_loc('split')] = 'test'
    return df


df = pd.read_csv('./data/raw_data/data/train.csv', names=['userID', 'itemID', 'rating'], header=0)

learner_id, course_id = 'userID', 'itemID'

min_u_num, min_i_num = 0, 0
        
filter_by_k_core(df)
df.reset_index(drop=True, inplace=True)

i_mapping_file = 'i_id_mapping.csv'
u_mapping_file = 'u_id_mapping.csv'

splitting = [0.7, 0.1, 0.2]
uid_field, iid_field = learner_id, course_id

uni_users = pd.unique(df[uid_field])
uni_items = pd.unique(df[iid_field])

# user와 item의 idmap dict 생성
u_id_map = {k: i for i, k in enumerate(uni_users)}
i_id_map = {k: i for i, k in enumerate(uni_items)}

df[uid_field] = df[uid_field].map(u_id_map)
df[iid_field] = df[iid_field].map(i_id_map)
df[uid_field] = df[uid_field].astype(int)
df[iid_field] = df[iid_field].astype(int)

# user와 item id mapping csv생성
rslt_dir = './data/dacon'
u_df = pd.DataFrame(list(u_id_map.items()), columns=['user_id', 'userID'])
i_df = pd.DataFrame(list(i_id_map.items()), columns=['asin', 'itemID'])

u_df.to_csv(os.path.join(rslt_dir, u_mapping_file), sep='\t', index=False)
i_df.to_csv(os.path.join(rslt_dir, i_mapping_file), sep='\t', index=False)
print(f'mapping dumped...')


# split data
df['split'] = df['rating']
data_split = df.groupby('userID').progress_apply(split_data)
data_split.reset_index(drop=True, inplace=True)
data_split['x_label'] = data_split['split'].map({'train' : 0, 'valid': 1, 'test' : 2})
x_label, rslt_file = 'x_label', './data/dacon/dacon1.inter'

# save inter file
temp_df = data_split[[learner_id, course_id, 'rating', x_label]]
print(f'columns: {temp_df.columns}')

temp_df.columns = [learner_id, course_id, 'rating', x_label]

temp_df.to_csv(rslt_file, sep='\t', index=False)

print(f'{rslt_file} saved')



        
