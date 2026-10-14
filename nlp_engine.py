import re
import pandas as pd

# Small offline dictionary for common English, Tamil and Tanglish query terms.
KEYWORD_MAP = {
    "student": ["education", "scholarship", "student", "school", "college", "skills"],
    "students": ["education", "scholarship", "student", "school", "college", "skills"],
    "scholarship": ["scholarship", "education", "student"],
    "study": ["education", "scholarship", "student"],
    "college": ["education", "scholarship", "college", "student"],
    "maanavar": ["education", "scholarship", "student", "college"],
    "kalvi": ["education", "scholarship", "student"],
    "padippu": ["education", "scholarship", "student"],
    "vivasayi": ["agriculture", "farmer", "kisan", "irrigation"],
    "vivasaayi": ["agriculture", "farmer", "kisan", "irrigation"],
    "vivasayam": ["agriculture", "farmer", "kisan"],
    "farmer": ["agriculture", "farmer", "kisan", "crop", "irrigation"],
    "agriculture": ["agriculture", "farmer", "kisan", "crop"],
    "pengal": ["women", "girl", "maternity", "working women"],
    "penkal": ["women", "girl", "maternity", "working women"],
    "women": ["women", "girl", "maternity", "working women"],
    "ponnu": ["women", "girl", "maternity"],
    "pension": ["pension", "senior citizen", "social security", "worker"],
    "old age": ["senior citizen", "old age", "pension"],
    "vayathaanavanga": ["senior citizen", "old age", "pension"],
    "health": ["health", "medical", "insurance", "hospital"],
    "maruthuvam": ["health", "medical", "insurance", "hospital"],
    "insurance": ["insurance", "health", "life insurance", "accident"],
    "job": ["employment", "skill", "career", "apprenticeship"],
    "velai": ["employment", "skill", "career", "job"],
    "velaivaippu": ["employment", "skill", "career", "job"],
    "business": ["business", "entrepreneurship", "credit", "msme"],
    "loan": ["credit", "loan", "business", "mudra"],
    "kadan": ["credit", "loan", "business"],
    "house": ["housing", "awas", "home"],
    "veedu": ["housing", "awas", "home"],
    "ration": ["food security", "ration", "foodgrain"],
    "gas": ["ujjwala", "lpg", "energy"],
    "matsyam": ["fisheries", "fishers"],
    "meenavar": ["fisheries", "fishers"],
    "disabled": ["disability", "disabilities", "assistive"],
    "maatuthiranali": ["disability", "disabilities", "assistive"],
    "transgender": ["transgender", "social justice"],
    "scheme": ["scheme"],
    "thittam": ["scheme"],
    "திட்டம்": ["scheme"],
    "மாணவர்": ["education", "scholarship", "student", "college"],
    "மாணவி": ["education", "scholarship", "student", "college", "girl"],
    "கல்வி": ["education", "scholarship", "student"],
    "விவசாயி": ["agriculture", "farmer", "kisan", "crop"],
    "விவசாயம்": ["agriculture", "farmer", "kisan"],
    "பெண்கள்": ["women", "girl", "maternity", "working women"],
    "பெண்": ["women", "girl", "maternity"],
    "முதியோர்": ["senior citizen", "old age", "pension"],
    "ஓய்வூதியம்": ["pension", "senior citizen", "social security"],
    "மருத்துவம்": ["health", "medical", "insurance", "hospital"],
    "வேலை": ["employment", "skill", "career", "job"],
    "கடன்": ["credit", "loan", "business"],
    "வீடு": ["housing", "awas", "home"],
    "உதவி": ["assistance", "support", "benefit", "scheme"],
}

def normalize_query(query: str) -> str:
    q = (query or "").lower().strip()
    additions = []
    for key, mapped in KEYWORD_MAP.items():
        if key in q:
            additions.extend(mapped)
    return q + " " + " ".join(additions)

def detect_language(query: str) -> str:
    if re.search(r"[\u0B80-\u0BFF]", query or ""):
        return "Tamil"
    tanglish_words = ["enna", "epdi", "venum", "thittam", "maanavar", "vivasayi", "pengal", "kadan"]
    return "Tanglish" if any(word in (query or "").lower() for word in tanglish_words) else "English"

def search_schemes(query: str, df: pd.DataFrame) -> pd.DataFrame:
    q = normalize_query(query)
    if not q.strip():
        return df.iloc[0:0].copy()
    searchable = df[["scheme_name", "category", "target_group", "benefit_summary", "eligibility_note", "government_level"]].fillna("").astype(str)
    scores = []
    q_terms = [t for t in re.findall(r"[\w\u0B80-\u0BFF]+", q.lower()) if len(t) > 1]
    for _, row in searchable.iterrows():
        text = " ".join(row.tolist()).lower()
        score = sum(2 if term in str(row["scheme_name"]).lower() else 1 for term in q_terms if term in text)
        scores.append(score)
    result = df.copy()
    result["_score"] = scores
    result = result[result["_score"] > 0].sort_values("_score", ascending=False)
    return result.drop(columns=["_score"])
