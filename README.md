# Audio-Mark

## 环境配置
安装ffmpeg
```shell
sudo apt install ffmpeg
```
创建虚拟环境
```shell
mamba create -n admk python=3.10
mamba activate admk
```
设置清华源（可选）
```shell
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```
安装依赖
```shell
pip install -r requirements.txt
```
安装pnpm
```shell
curl -fsSL https://get.pnpm.io/install.sh | sh -
pnpm env use --global lts
```

## 启动前端
```shell
cd ui/
pnpm install
pnpm run dev
```

## 启动后端
```shell
pip install -r requirements.txt
python main.py
```