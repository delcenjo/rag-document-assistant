from .config import CHAT_MODEL

SYSTEM_PROMPT = (
    "You answer questions using only the provided context. "
    "If the answer is not contained in the context, say you don't know. "
    "Cite the source filename in square brackets after each fact you use."
)


def build_prompt(question, contexts):
    context_block = "\n\n".join(f"[{chunk['source']}]\n{chunk['text']}" for chunk, _ in contexts)
    return f"Context:\n{context_block}\n\nQuestion: {question}"


def generate_answer(question, contexts, model=CHAT_MODEL):
    import anthropic

    client = anthropic.Anthropic()
    message = client.messages.create(
        model=model,
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_prompt(question, contexts)}],
    )
    return message.content[0].text
