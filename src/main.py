# coding: utf-8
# @email: enoche.chow@gmail.com

"""
Main entry
# UPDATED: 2022-Feb-15
##########################
"""

import os
import argparse
from utils.quick_start import quick_start
from utils.quick_start import quick_start_val_only
os.environ['NUMEXPR_MAX_THREADS'] = '48'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '-m', type=str, default='BM3', help='name of models')
    parser.add_argument('--dataset', '-d', type=str, default='dacon', help='name of datasets')
    parser.add_argument('--val-only', action="store_true")
    parser.add_argument('--best-ckpt', type=str, default='./model_ckpt/bestmodel_100.ckpt', help='input your beckckpt dirs')

    config_dict = {
        'gpu_id': 0,
    }

    args, _ = parser.parse_known_args()

    if args.val_only:
        quick_start_val_only(model=args.model, dataset=args.dataset, config_dict=config_dict, ckpt_path=args.best_ckpt)
    else:
        quick_start(model=args.model, dataset=args.dataset, config_dict=config_dict, save_model=True)


