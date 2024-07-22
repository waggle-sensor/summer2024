conda create -n AWQ-VILA python=3.10 -y
conda activate AWQ-VILA
pip install --upgrade pip

git clone https://github.com/NVlabs/VILA
cd VILA
pip install -e .
cd ..

git clone -b nv_laptop https://github.com/mit-han-lab/llm-awq
cd llm-awq
bash install.sh
cd vila_helper

bash download_vila.sh VILA1.5-7b-AWQ

bash vila_launcher.sh VILA1.5-7b-AWQ/
