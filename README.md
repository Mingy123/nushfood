# NUSHFood

Download the model_final.pth file from your google drive and put in Weights
Install torch first by `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu`
Install detectron by running `pip install 'git+https://github.com/facebookresearch/detectron2.git'`
Finally finish everything via `pip install -r requirements.txt`  
  
Test segment via `curl -X POST -F "file=@PXL_20240319_054302775.jpg" localhost:5000/segment`