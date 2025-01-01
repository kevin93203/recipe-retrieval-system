# recipe-retrieval-system


#Install Tools

> pip uninstall torch torchvision  
> pip install -r ./requirement  
> pip install git+https://github.com/openai/CLIP.git  

#Download Database
> python icook_recipe

#Execute Backend  
> backend\fastAPI dev



#Execute FrontEnd  
> frontend\npm run dev
  
Web backend Server:  http://127.0.0.1:8000/
Web frontend Server :  http://127.0.0.1:5173/




## Notice
完全重設環境方式：

1. 建立全新的 conda 環境（使用 Python 3.10 以確保最佳相容性）：
```bash
conda create -n recipe_env python=3.10
conda activate recipe_env
```

2. 使用 conda 安裝主要套件：
```bash
conda install -c pytorch pytorch torchvision torchaudio cpuonly
conda install -c conda-forge transformers
conda install -c conda-forge sentence-transformers
```

3. 安裝其他需要的套件：
```bash
conda install -c conda-forge gensim
conda install -c conda-forge jieba
conda install -c conda-forge fastapi uvicorn
```

4. 安裝 CLIP：
```bash
pip install git+https://github.com/openai/CLIP.git
```
