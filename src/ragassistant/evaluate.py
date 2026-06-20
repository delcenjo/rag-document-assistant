from .config import TOP_K
from .retriever import Retriever

EVAL_SET = [
    {"question": "How much does the Pro plan cost?", "source": "pricing.md"},
    {"question": "What encryption is used for data at rest?", "source": "security.md"},
    {"question": "What is the API rate limit on the Free plan?", "source": "api.md"},
    {"question": "How can I export my notes?", "source": "faq.md"},
    {"question": "Does Nimbus Notes work offline?", "source": "faq.md"},
    {"question": "Which platforms are supported?", "source": "overview.md"},
    {"question": "How do I cancel my subscription?", "source": "pricing.md"},
    {"question": "Is Nimbus Notes SOC 2 compliant?", "source": "security.md"},
]


def main():
    retriever = Retriever()
    hits = 0
    for item in EVAL_SET:
        results = retriever.retrieve(item["question"], TOP_K)
        sources = [chunk["source"] for chunk, _ in results]
        hit = item["source"] in sources
        hits += hit
        print(f"[{'ok  ' if hit else 'MISS'}] {item['question']}  ->  {sources}")
    recall = hits / len(EVAL_SET)
    print(f"\nRetrieval recall@{TOP_K}: {recall:.2f} ({hits}/{len(EVAL_SET)})")
    return recall


if __name__ == "__main__":
    main()
