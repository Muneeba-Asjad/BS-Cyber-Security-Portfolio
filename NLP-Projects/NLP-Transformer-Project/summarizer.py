from groq_client import ask_groq

print("======================================")
print(" Text Summarization using Groq ")
print("======================================")

while True:

    text = input("\nEnter Text (type 'exit' to quit): ").strip()

    if text.lower() == "exit":
        print("\nProgram Closed Successfully!")
        break

    if text == "":
        print("Please enter some text.")
        continue

    prompt = f"""
Summarize the following text in 4 to 5 lines.

Text:
{text}
"""

    print("\nGenerating Summary...\n")

    summary = ask_groq(prompt)

    print("Summary")
    print("----------------------------------------")
    print(summary)