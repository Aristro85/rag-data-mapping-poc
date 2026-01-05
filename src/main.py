from src.llm import get_llm
import sys

print("Current sys.path:")
print(sys.path)


def main():
    llm = get_llm()
    response = llm.invoke("Explain RAG in 3 bullet points under 200 words in total.")
    print(response.content)

if __name__ == "__main__":
    main()