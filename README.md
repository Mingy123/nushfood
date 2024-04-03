# NUSHFood

Download the model_final.pth file from your google drive and put in Weights
Install torch first by `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu`
Then run `pip install -r requirements.txt`

Start nginx:  
`sudo cp nginx.conf /etc/nginx/`  
`sudo systemctl start nginx`  
or equivalent for your system
 
Test segment via `curl -X POST -F "file=@PXL_20240319_054302775.jpg" localhost/api/segment`
