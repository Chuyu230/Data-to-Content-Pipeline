# 海外来华医疗项目：第三部分最终版

这个版本已经按你上传的根目录结构对齐：

- `analyze/analysis_outputs/`
- `analyze/promo_outputs/`
- `content/generate_multi_platform_content.py`
- `data/cleaned/`

根目录结构来自你上传的 `list.txt`。fileciteturn4file0

## 一、脚本做什么

`content/generate_multi_platform_content.py` 会读取：

- `analyze/promo_outputs/promo_user.csv`
- `analyze/promo_outputs/promo_soft.csv`
- `analyze/analysis_outputs/refined_top_keywords.csv`
- `analyze/analysis_outputs/refined_demand_category_counts.csv`

然后自动生成：

- 多平台文案：X / Instagram / Facebook
- 多风格文案：educational / storytelling / premium_branding
- 图片提示词：`image_prompt`
- 可选真实图片生成：仅 OpenAI
- 合规扫描：标记绝对化和高风险医疗营销表述

输出目录为：

- `generation/prompt_bank.csv`
- `generation/generated_posts.csv`
- `generation/generated_posts.jsonl`
- `generation/generated_images/`（开启 OpenAI 图片生成时）
- `generation/run_config.json`

---

## 二、安装依赖：详细步骤

下面分别给 Windows 和 Conda 两种常见方式。

### 方案 A：Windows + venv（推荐）

#### 1）确认你已经安装 Python 3.10+
在命令行输入：

```bash
python --version
```

如果没有显示版本，先安装 Python，并勾选 **Add Python to PATH**。

#### 2）进入你的项目根目录
例如：

```bash
cd C:\your_project_root
```

你的根目录里应该能看到：

- `analyze`
- `content`
- `data`
- `list.txt`

#### 3）创建虚拟环境

```bash
python -m venv .venv
```

#### 4）激活虚拟环境

PowerShell：

```bash
.\.venv\Scripts\Activate.ps1
```

CMD：

```bash
.\.venv\Scripts\activate.bat
```

如果 PowerShell 报执行策略错误，可以先运行：

```bash
Set-ExecutionPolicy -Scope Process Bypass
```

然后再次激活。

#### 5）安装依赖
把 `requirements.txt` 放到项目根目录后执行：

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 6）复制环境变量文件
把 `.env.example` 复制成 `.env`

PowerShell：

```bash
Copy-Item .env.example .env
```

CMD：

```bash
copy .env.example .env
```

#### 7）编辑 `.env`
最少要改这几项：

```env
PROJECT_ROOT=C:\your_project_root
LLM_PROVIDER=openai
OPENAI_API_KEY=你的key
LLM_MODEL=gpt-4.1-mini
```

如果你用 DeepSeek：

```env
PROJECT_ROOT=C:\your_project_root
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=你的key
LLM_MODEL=deepseek-chat
LLM_BASE_URL=https://api.deepseek.com
```

#### 8）把脚本放到 `content/` 目录
确保最终脚本路径是：

```text
content/generate_multi_platform_content.py
```

#### 9）运行脚本

```bash
python content/generate_multi_platform_content.py
```

#### 10）开启图片生成
仅 OpenAI 支持直接生成图片文件：

```env
ENABLE_IMAGE_GENERATION=true
IMAGE_MODEL=gpt-image-1
```

再运行：

```bash
python content/generate_multi_platform_content.py --image-generation
```

#### 11）开启多语言

```env
ENABLE_MULTILINGUAL=true
OUTPUT_LANGUAGES=en,zh
```

或命令行：

```bash
python content/generate_multi_platform_content.py --multilingual
```

---

### 方案 B：Conda

#### 1）创建环境

```bash
conda create -n medcontent python=3.11 -y
conda activate medcontent
```

#### 2）安装依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3）复制 `.env` 并填写

同上。

#### 4）运行

```bash
python content/generate_multi_platform_content.py
```

---

## 三、脚本运行参数

### 基础运行

```bash
python content/generate_multi_platform_content.py
```

### 开启图片生成

```bash
python content/generate_multi_platform_content.py --image-generation
```

### 开启多语言

```bash
python content/generate_multi_platform_content.py --multilingual
```

### 同时开启

```bash
python content/generate_multi_platform_content.py --multilingual --image-generation
```

---

## 四、常见报错与解决

### 1）`Missing API key`
说明 `.env` 里没填对 key。

检查：

- `OPENAI_API_KEY`
- 或 `DEEPSEEK_API_KEY`
- `LLM_PROVIDER`

### 2）`Missing file`
说明前两部分的输出文件没有放在脚本预期位置。

检查这些文件是否存在：

- `analyze/promo_outputs/promo_user.csv`
- `analyze/promo_outputs/promo_soft.csv`
- `analyze/analysis_outputs/refined_top_keywords.csv`
- `analyze/analysis_outputs/refined_demand_category_counts.csv`

### 3）PowerShell 无法激活 venv
运行：

```bash
Set-ExecutionPolicy -Scope Process Bypass
```

### 4）OpenAI 图片生成失败
先确认：

- `LLM_PROVIDER=openai`
- `ENABLE_IMAGE_GENERATION=true`
- `IMAGE_MODEL=gpt-image-1`

DeepSeek 路径目前只生成 `image_prompt`，不会直接输出图片文件。

---

## 五、建议的落地顺序

先跑纯文本：

```bash
python content/generate_multi_platform_content.py
```

确认 `generation/generated_posts.csv` 正常。

然后再开启：

```bash
python content/generate_multi_platform_content.py --image-generation
```

