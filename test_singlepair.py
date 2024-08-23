
import cv2
import numpy as np
import json
import os
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib
import argparse

from AMS_Former import matcher

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


def match():

    mod1_img = cv2.cvtColor(cv2.imread(mod1_path), cv2.COLOR_BGR2RGB)
    mod2_img = cv2.imread(mod2_path)
    
    mkpts0, mkpts1, runtime = matcher(img1_path=mod1_path, img2_path=mod2_path, mode = mode, device = device)

    NOM = mkpts0.shape[0]

    color_mask = np.full(NOM, True)

    color = ['blue' if color_i else 'red' for color_i in color_mask]
    make_matching_figure(mod1_img, mod2_img, mkpts0=mkpts0, mkpts1=mkpts1,
                                color=color, path = result_path)
    
    print(f'run_time: {str(runtime)}, NOM: {str(NOM)}')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-ref_path', type=str, default = '' , help='reference image dir')
    parser.add_argument('-sen_path', type=str, default = '' , help='sensed image dir')

    parser.add_argument('-result_path', type=str, default = '' , help='match result')
    parser.add_argument('--mode', type=str, default = 'mode2' , choices=['mode1', 'mode2', 'mode3', 'mode4',],
                        help='mode1: rs_rgb_nir, mode2: rs_rgb_map, mode3: cv_rgb_inf, mode4: cv_rgb_nir')

    parser.add_argument('--device', type=str, default = 'cuda' , help='device')

    args = parser.parse_args()

    mod1_path = args.ref_path
    mod2_path = args.sen_path
    result_path = args.result_path
    mode = args.mode
    device = args.device

    match()