# AMS_Former
This is the official code for AMS_Former. https://www.sciencedirect.com/science/article/pii/S0924271626000213
![AMS-Former](framework.png)

# Results
![results](results.png)

## Installation (Only Linux)

```pip install -r requirements.txt```

# Download weights

Download datasets: https://pan.baidu.com/s/1Q5cplJHkHxBHcXBKdcP6qA?pwd=5gdy

Please download and extract it, then rename `AMS_weights` to `weights` and place it in the project root directory.


# Download datasets
https://pan.baidu.com/s/1Ku1Aya9prYw-fsAYCcAkiQ?pwd=z4jb

# Test

For RGB-NIR:
``` python test.py --ref_dir datasets/RGB-NIR/RGB --sen_dir datasets/RGB-NIR/NIR --json_path datasets/RGB-NIR/trans_info.json --results_dir results/RGB-NIR --mode mode1```
The results will be saved at "results/RGB-NIR"

For SGM-SM:
``` python test.py --ref_dir datasets/SGM-SM/SGM --sen_dir datasets/SGM-SM/SM --json_path datasets/SGM-SM/trans_info.json --results_dir results/SGM-SM --mode mode2```
The results will be saved at "results/SGM-SM"

For RGB-LWIR:
``` python test.py --ref_dir datasets/RGB-LWIR/RGB --sen_dir datasets/RGB-LWIR/LWIR --json_path datasets/RGB-LWIR/trans_info.json --results_dir results/RGB-LWIR --mode mode3```
The results will be saved at "results/RGB-NIR"

For RGB-Ndepth:
``` python test.py --ref_dir datasets/RGB-Ndepth/RGB --sen_dir datasets/RGB-Ndepth/Ndepth --json_path datasets/RGB-Ndepth/trans_info.json --results_dir results/RGB-Ndepth --mode mode1```
The results will be saved at "results/RGB-NIR"

For RGB-RGB:
``` python test.py --ref_dir datasets/RGB-RGB/RGB1 --sen_dir datasets/RGB-RGB/RGB2 --json_path datasets/RGB-RGB/trans_info.json --results_dir results/RGB-RGB --mode mode1```
The results will be saved at "results/RGB-RGB"

## Thank you！
If you find our code useful, please consider adding the following citation:

```bibtex
@article{RAO2026957,
title = {AMS-Former: Adaptive multi-scale transformer for multi-modal image matching},
journal = {ISPRS Journal of Photogrammetry and Remote Sensing},
volume = {232},
pages = {957-973},
year = {2026},
issn = {0924-2716},
author = {Jiahao Rao and Rui Liu and Jianjun Guan and Xin Tian},
}
