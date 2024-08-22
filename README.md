# AMS_Former
This is the official code for AMS_Former.
# Installation
```python==3.8, einops==0.3.0, cryptography==43.0.0, torch==2.3.0```

# Download weights
Download weights : https://pan.baidu.com/s/1g5qGGKq3DLQFX1d-NoUPUQ (password：p1iq). 
Please extract it and place it in the main directory.
# Download datasets
Dwonload datasets：https://pan.baidu.com/s/1hB4KJF8zs20SLdgBDV9-vw  (password: 9y3t). 
Please extract it and place it in the main directory.
# Test
You can run test.py to generate test results.

```python test.py --ref_dir dataset/rs_rgb_map/rgb --sen_dir dataset/rs_rgb_map/map --json_path dataset/rs_rgb_map/trans_info.json --result_dir results/rs_rgb_map --mode mode2 --device cuda```

You can run the following commands to generate other results.

```python test.py --ref_dir dataset/rs_rgb_nir/rgb --sen_dir dataset/rs_rgb_nir/nir --json_path dataset/rs_rgb_nir/trans_info.json --result_dir results/rs_rgb_nir --mode mode1 --device cuda```

```python test.py --ref_dir dataset/cv_rgb_inf/rgb --sen_dir dataset/cv_rgb_inf/inf --json_path dataset/cv_rgb_inf/trans_info.json --result_dir results/cv_rgb_inf --mode mode3 --device cuda```

```python test.py --ref_dir dataset/cv_rgb_nir/rgb --sen_dir dataset/cv_rgb_nir/nir --json_path dataset/cv_rgb_nir/trans_info.json --result_dir results/cv_rgb_nir --mode mode4 --device cuda```
