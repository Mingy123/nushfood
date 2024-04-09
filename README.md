# NUSHFood

Download the models at https://drive.google.com/file/d/1JquD0_Bbpel7X5cA5ZwTtcE1Ey3kA-DK/view?usp=sharing and https://drive.google.com/file/d/137TlEActhl1NM8OvzQzVnrxCPm0vI7vA/view?usp=sharing. Place them both in the root folder.

THIS WILL NOT RUN ON WINDOWS.

Install torch first by `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu` (Skips downloading CUDA drivers)
Install tensorflow by doing `pip3 install tensorflow-cpu`
Finally install everything else by running `pip3 install -r requirements.txt`

Start nginx:  
`sudo cp server* /etc/nginx/`
`sudo cp nginx.conf /etc/nginx/`  
`sudo systemctl start nginx`  
or equivalent for your system.
 
Then access `https://localhost` and bypass the error warning to use the system!
