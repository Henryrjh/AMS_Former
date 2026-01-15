
import cv2
import numpy as np
import json
import os
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib
import argparse
from datetime import datetime, timedelta, timezone
from scipy.io import savemat


from AMS_Former.AMS_Former import matcher

def location_error(pt0, pt1, H):
    ### H: the GT pts0--->pts1
    pt1_gt = cv2.perspectiveTransform(np.array([[pt0]]), H)   ### [w,h]
    error = np.linalg.norm(pt1_gt[0][0] - pt1)
    return error


def make_matching_figure(
        img0, img1, mkpts0, mkpts1, color,
        kpts0=None, kpts1=None, dpi=75, path=None):
    # draw image pair
    plt.switch_backend('agg')
    assert mkpts0.shape[0] == mkpts1.shape[0], f'mkpts0: {mkpts0.shape[0]} v.s. mkpts1: {mkpts1.shape[0]}'
    fig, axes = plt.subplots(1, 2, figsize=(10, 6), dpi=dpi)
    axes[0].imshow(img0, cmap='gray')
    axes[1].imshow(img1, cmap='gray')
    for i in range(2):   # clear all frames
        axes[i].get_yaxis().set_ticks([])
        axes[i].get_xaxis().set_ticks([])
        for spine in axes[i].spines.values():
            spine.set_visible(False)
    plt.tight_layout(pad=1)
    
    if kpts0 is not None:
        assert kpts1 is not None
        axes[0].scatter(kpts0[:, 0], kpts0[:, 1], c='w', s=2)
        axes[1].scatter(kpts1[:, 0], kpts1[:, 1], c='w', s=2)

    # draw matches
    if mkpts0.shape[0] != 0 and mkpts1.shape[0] != 0:
        fig.canvas.draw()
        transFigure = fig.transFigure.inverted()
        fkpts0 = transFigure.transform(axes[0].transData.transform(mkpts0))
        fkpts1 = transFigure.transform(axes[1].transData.transform(mkpts1))
        fig.lines = [matplotlib.lines.Line2D((fkpts0[i, 0], fkpts1[i, 0]),
                                            (fkpts0[i, 1], fkpts1[i, 1]),
                                            transform=fig.transFigure, c=color[i], linewidth=1)
                                        for i in range(len(mkpts0))]
        
        axes[0].scatter(mkpts0[:, 0], mkpts0[:, 1], c=color, s=4)
        axes[1].scatter(mkpts1[:, 0], mkpts1[:, 1], c=color, s=4)
    # save or return figure
    if path:
        plt.savefig(str(path), bbox_inches='tight', pad_inches=0)
        plt.close()
    else:
        return fig


def match_statistic():

    with open(json_path, 'r') as f:
        H_gts = json.load(f)

    os.makedirs(visual_dir, exist_ok=True)

    header = ['NOM', 'NCM', 'RMSE', 'MA']
    filenames = os.listdir(input_dir[0])
    metircs_df = pd.DataFrame(index=filenames, columns=header)
    metircs_df.index.set_names('Filename', inplace=True)

    total = len(os.listdir(input_dir[0]))
    count = 0
    total_time = 0
    total_NOM = 0
    total_NCM = 0
    total_RMSE = 0
    N_SR = 0

    for filename in os.listdir(input_dir[0]):
        mod1_path = os.path.join(input_dir[0], filename)
        mod2_path = os.path.join(input_dir[1], filename)

        mod1_img = cv2.cvtColor(cv2.imread(mod1_path), cv2.COLOR_BGR2RGB)
        mod2_img = cv2.imread(mod2_path)

        H_gt = np.array(H_gts[filename]['H'])
        visual_path = os.path.join(visual_dir, filename)
        
        mkpts0, mkpts1, runtime = matcher(img1_path=mod1_path, img2_path=mod2_path, mode = mode, device = device)

        save_mat_path = os.path.join(visual_dir, os.path.splitext(filename)[0] + ".mat")
        savemat(save_mat_path, {'mkpts0': mkpts0, 'mkpts1': mkpts1})

        total_time += runtime

        NOM = mkpts0.shape[0]
        NCM = 0
        RMSE_squre = 0
        color_mask = np.full(NOM, False)

        for i in range(mkpts0.shape[0]):
            pt0 = mkpts0[i]
            pt1 = mkpts1[i]
            l_e = location_error(pt0, pt1, H_gt)
            RMSE_squre += l_e ** 2
            if l_e < match_thresold:
                NCM += 1
                color_mask[i] = True
        
        if NOM == 0:
            RMSE = 0
            precision = 0
        else:
            RMSE = math.sqrt(RMSE_squre / NOM)
            precision = NCM / NOM

        color = ['blue' if color_i else 'yellow' for color_i in color_mask]
        make_matching_figure(mod1_img, mod2_img, mkpts0=mkpts0, mkpts1=mkpts1,
                                 color=color, path = visual_path)
        count  = count + 1
        total_NOM += NOM
        total_NCM += NCM
        total_RMSE += RMSE

        if (RMSE > 0) and (RMSE < 5):
            N_SR += 1

        metircs_df.loc[filename] = {'NOM': NOM, 'NCM': NCM, 'RMSE': RMSE, 'MA': precision, 'SR':None }
        print(f'Filename: {filename}, NOM: {str(NOM)}, NCM: {str(NCM)}, RMSE: {str(RMSE)}, MA: {str(precision)}, {str(count)}-th in {str(total)}, Time: {str(runtime)} ')
    
    metircs_df.to_csv(metrics_csv)
    
    avg_runtime = total_time / len(os.listdir(input_dir[0]))

    avg_NOM = total_NOM / len(os.listdir(input_dir[0]))
    avg_NCM = total_NCM / len(os.listdir(input_dir[0]))
    avg_pre = avg_NCM / avg_NOM
    avg_RMSE = total_RMSE / len(os.listdir(input_dir[0]))
    SR = N_SR / len(os.listdir(input_dir[0]))

    avg_row = pd.DataFrame({
        'Filename': ['Average'],     
        'NOM': [avg_NOM],
        'NCM': [avg_NCM],
        'RMSE': [avg_RMSE],
        'MA': [avg_pre],
        'SR': [SR]
    })
    metircs_df = pd.concat([metircs_df, avg_row])
    metircs_df.to_csv(metrics_csv)


    print(f'AVG_time: {str(avg_runtime)}, AVG_NOM: {str(avg_NOM)}, AVG_NCM: {str(avg_NCM)}, AVG_MA: {str(avg_pre)}, AVG_RMSE: {str(avg_RMSE)}, SR: {str(SR)}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--ref_dir', type=str, default = '' , help='reference image dir')
    parser.add_argument('--sen_dir', type=str, default = '' , help='sensed image dir')
    parser.add_argument('--json_path', type=str, default = 'trans_info.json' , help='transformation matrix')
    
    parser.add_argument('--result_dir', type=str, default = 'results' , help='output dir')
    parser.add_argument('--mode', type=str, default = 'mode1' , choices=['mode1', 'mode2', 'mode3',],
                        help='mode1: RGB-NIR, ' \
                            'mode2: SGM-SM, ' \
                            'mode3: RGB-LWIR, ' \
                            )
    
    parser.add_argument('--match_thresold', type=int, default = 3 , help='match_thresold')
    parser.add_argument('--device', type=str, default = 'cuda' , help='device')

    args = parser.parse_args()

    result_dir = args.result_dir
    visual_dir = os.path.join(result_dir, 'visual')
    metrics_csv = os.path.join(result_dir, 'metrics.csv')
    json_path = args.json_path
    input_dir = [args.ref_dir, args.sen_dir]
    match_thresold = args.match_thresold
    mode = args.mode
    device = args.device

    china_tz = timezone(timedelta(hours=8))
    now = datetime.now(china_tz)
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
    print(f"当前时间（中国时间）：{formatted_time}")
    
    match_statistic()

    china_tz = timezone(timedelta(hours=8))
    now = datetime.now(china_tz)
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
    print(f"当前时间（中国时间）：{formatted_time}")