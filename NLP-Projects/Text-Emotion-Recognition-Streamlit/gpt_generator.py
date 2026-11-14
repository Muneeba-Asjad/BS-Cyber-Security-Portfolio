from groq_client import ask_groq

print("======================================")
print(" NLP Text Generation using Groq ")
print("======================================")

while True:

    prompt = input("\nEnter Prompt (type 'exit' to quit): ").strip()

    if prompt.lower() == "exit":
        print("\nProgram Closed Successfully!")
        break

    if prompt == "":
        print("Please enter a prompt.")
        continue

    print("\nGenerating...\n")

    answer = ask_groq(prompt)

    print("AI Response")
    print("----------------------------------------")
    print(answer)