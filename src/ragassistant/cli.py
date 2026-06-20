import argparse
import os

from dotenv import load_dotenv

from .config import TOP_K
from .generator import generate_answer
from .retriever import Retriever


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Ask questions about the indexed corpus")
    parser.add_argument("question", nargs="?", help="question to ask")
    parser.add_argument("--top-k", type=int, default=TOP_K)
    parser.add_argument("--show-context", action="store_true", help="print retrieved chunks")
    args = parser.parse_args()

    question = args.question or input("Question: ")
    contexts = Retriever().retrieve(question, args.top_k)

    if args.show_context or not os.getenv("ANTHROPIC_API_KEY"):
        print("\nRetrieved context:")
        for chunk, score in contexts:
            print(f"  [{chunk['source']}] score={score:.3f}")

    if os.getenv("ANTHROPIC_API_KEY"):
        print("\nAnswer:")
        print(generate_answer(question, contexts))
    else:
        print("\nSet ANTHROPIC_API_KEY (see .env.example) to generate a written answer.")


if __name__ == "__main__":
    main()
