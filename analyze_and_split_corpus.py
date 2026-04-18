import pandas as pd
import re
import os
from collections import Counter
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import matplotlib.pyplot as plt

# ========= 项目路径 =========
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ========= 输入 =========
CLEANED_DIR = os.path.join(BASE_DIR, "data", "cleaned")
INPUT_PATH = os.path.join(CLEANED_DIR, "all_platforms_cleaned.csv")

# ========= 输出（你刚刚定的结构） =========
ANALYZE_DIR = os.path.join(BASE_DIR, "analyze")

PROMO_DIR = os.path.join(ANALYZE_DIR, "promo_outputs")
ANALYSIS_DIR = os.path.join(ANALYZE_DIR, "analysis_outputs")
FIGURES_DIR = os.path.join(ANALYSIS_DIR, "figures")

# 创建目录
os.makedirs(PROMO_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

# ========= 输入 =========
INPUT_PATH = os.path.join(CLEANED_DIR, "all_platforms_cleaned.csv")

# ========= 语料输出 =========
REAL_USER_PATH = os.path.join(PROMO_DIR, "real_user_comments.csv")
PROMO_STRONG_PATH = os.path.join(PROMO_DIR, "promo_strong.csv")
PROMO_USER_PATH = os.path.join(PROMO_DIR, "promo_user.csv")
PROMO_SOFT_PATH = os.path.join(PROMO_DIR, "promo_soft.csv")

# ========= 分析输出 =========
REFINED_REAL_USER_PATH = os.path.join(ANALYSIS_DIR, "refined_real_user_comments.csv")
CATEGORY_COUNT_PATH = os.path.join(ANALYSIS_DIR, "refined_demand_category_counts.csv")
TOP_KEYWORDS_PATH = os.path.join(ANALYSIS_DIR, "refined_top_keywords.csv")

# ========= 图表输出 =========
DEMAND_FIG_PATH = os.path.join(FIGURES_DIR, "refined_demand_distribution.png")
KEYWORD_FIG_PATH = os.path.join(FIGURES_DIR, "refined_top_keywords.png")


# ========= 第一部分：营销 / 真实用户分类 =========
def classify_promo(text):
    text = str(text).lower()

    # 强营销（机构/广告）
    if any(k in text for k in [
        "our clinic", "our hospital", "we provide", "contact us",
        "book now", "consultation", "dm us", "whatsapp",
        "treatment package", "international patient service"
    ]):
        return "promo_strong"

    # 用户推荐
    if any(k in text for k in [
        "i went to", "i did", "i got", "i recommend",
        "worth it", "saved", "cheaper", "cost me",
        "better than", "fraction of the cost"
    ]):
        return "promo_user"

    # 弱营销
    if any(k in text for k in [
        "best hospital", "affordable treatment",
        "high quality care", "top clinic",
        "medical tourism destination"
    ]):
        return "promo_soft"

    return "real_user"


# ========= 第二部分：需求分析 =========
DEMAND_CATEGORIES = {
    "cost_affordability": [
        "cost", "price", "cheap", "cheaper", "expensive",
        "afford", "affordable", "paid", "pay", "save", "saved",
        "worth", "pricey", "too much", "budget"
    ],
    "quality_trust": [
        "good", "bad", "best", "trust", "reliable",
        "experience", "recommend", "review", "quality",
        "reputation", "qualified", "safe", "safety"
    ],
    "screening_checkup": [
        "screening", "checkup", "check", "scan",
        "mri", "ct", "pet", "blood test", "test",
        "diagnosis", "early detection", "colonoscopy"
    ],
    "insurance_payment": [
        "insurance", "covered", "coverage", "copay",
        "deductible", "out of pocket", "payment"
    ],
    "travel_logistics": [
        "travel", "flight", "trip", "visa", "hotel",
        "overseas", "international", "mexico", "turkey",
        "china", "border"
    ],
    "risk_complications": [
        "risk", "problem", "issue", "complication",
        "infection", "unsafe", "danger", "fraud", "fraudulent"
    ],
    "recovery_followup": [
        "recovery", "aftercare", "healing",
        "follow up", "follow-up", "post op", "post-op"
    ]
}

IRRELEVANT_PATTERNS = [
    r"\bthanks\b",
    r"\bthank you\b",
    r"\bthanks for the information\b",
    r"\bi'm sorry\b",
    r"\bsorry for your loss\b",
    r"\bpraying for\b",
]

CUSTOM_STOPWORDS = {
    "medical", "tourism", "health", "abroad", "treatment",
    "hospital", "hospitals", "doctor", "doctors", "country",
    "countries", "patient", "patients", "people", "medical",
    "cancer", "just", "don", "did", "does", "need", "good",
    "really", "make", "think", "know", "want", "one",
    "like", "get", "got", "going", "would", "could", "also",
    "year", "years", "time"
}

STOPWORDS = set(ENGLISH_STOP_WORDS).union(CUSTOM_STOPWORDS)


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def is_irrelevant(text):
    t = text.lower().strip()
    if len(t.split()) < 5:
        return True
    for p in IRRELEVANT_PATTERNS:
        if re.search(p, t):
            return True
    return False


def classify_demand(text):
    matched = []
    for category, keywords in DEMAND_CATEGORIES.items():
        if any(k in text for k in keywords):
            matched.append(category)
    return matched


def get_top_keywords(texts, top_n=20):
    words = []
    for t in texts:
        t = clean_text(t)
        tokens = [w for w in t.split() if w not in STOPWORDS and len(w) > 2]
        words.extend(tokens)
    return Counter(words).most_common(top_n)


def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"找不到输入文件: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)

    if "text_clean" not in df.columns:
        raise ValueError("输入文件中缺少 text_clean 列")

    print("读取成功，总条数:", len(df))

    # ========= Step 1: 营销 / 真实用户分类 =========
    df["promo_type"] = df["text_clean"].apply(classify_promo)

    real_df = df[df["promo_type"] == "real_user"].copy()
    strong_df = df[df["promo_type"] == "promo_strong"].copy()
    user_df = df[df["promo_type"] == "promo_user"].copy()
    soft_df = df[df["promo_type"] == "promo_soft"].copy()

    real_df.to_csv(REAL_USER_PATH, index=False, encoding="utf-8-sig")
    strong_df.to_csv(PROMO_STRONG_PATH, index=False, encoding="utf-8-sig")
    user_df.to_csv(PROMO_USER_PATH, index=False, encoding="utf-8-sig")
    soft_df.to_csv(PROMO_SOFT_PATH, index=False, encoding="utf-8-sig")

    print("\n=== 营销语料分类统计 ===")
    print(df["promo_type"].value_counts())

    # ========= Step 2: 对真实用户评论做需求分析 =========
    real_df["text"] = real_df["text_clean"].fillna("").astype(str)
    real_df["text_norm"] = real_df["text"].apply(clean_text)

    # 去明显无关
    refined_df = real_df[~real_df["text_norm"].apply(is_irrelevant)].copy()

    # 只保留至少命中1个需求类别的
    refined_df["categories"] = refined_df["text_norm"].apply(classify_demand)
    refined_df = refined_df[refined_df["categories"].apply(len) > 0].copy()
    refined_df["categories_str"] = refined_df["categories"].apply(lambda x: "; ".join(x))

    # 统计类别
    all_cats = []
    for cats in refined_df["categories"]:
        all_cats.extend(cats)

    cat_count = Counter(all_cats)
    cat_df = pd.DataFrame(cat_count.items(), columns=["category", "count"]).sort_values("count", ascending=False)

    # 高频词
    word_df = pd.DataFrame(get_top_keywords(refined_df["text_norm"], 20), columns=["keyword", "count"])

    # 保存分析结果
    refined_df.to_csv(REFINED_REAL_USER_PATH, index=False, encoding="utf-8-sig")
    cat_df.to_csv(CATEGORY_COUNT_PATH, index=False, encoding="utf-8-sig")
    word_df.to_csv(TOP_KEYWORDS_PATH, index=False, encoding="utf-8-sig")

    # 图1：需求分布
    plt.figure()
    plt.bar(cat_df["category"], cat_df["count"])
    plt.xticks(rotation=45)
    plt.title("Refined User Demand Distribution")
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(DEMAND_FIG_PATH)
    plt.close()

    # 图2：关键词
    plt.figure()
    plt.bar(word_df["keyword"], word_df["count"])
    plt.xticks(rotation=45)
    plt.title("Refined Top Keywords")
    plt.xlabel("Keyword")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(KEYWORD_FIG_PATH)
    plt.close()

    print("\n=== 需求分析结果 ===")
    print("原始真实用户条数:", len(real_df))
    print("过滤后条数:", len(refined_df))
    print("\n需求类别统计：")
    print(cat_df)
    print("\n关键词 Top 20：")
    print(word_df.head(20))

    print("\n✅ 已输出：")
    print("语料库：")
    print(f"- {REAL_USER_PATH}")
    print(f"- {PROMO_STRONG_PATH}")
    print(f"- {PROMO_USER_PATH}")
    print(f"- {PROMO_SOFT_PATH}")
    print("分析结果：")
    print(f"- {REFINED_REAL_USER_PATH}")
    print(f"- {CATEGORY_COUNT_PATH}")
    print(f"- {TOP_KEYWORDS_PATH}")
    print("图表：")
    print(f"- {DEMAND_FIG_PATH}")
    print(f"- {KEYWORD_FIG_PATH}")


if __name__ == "__main__":
    main()