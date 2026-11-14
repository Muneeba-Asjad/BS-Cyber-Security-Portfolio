import spacy

print("Loading spaCy Model...")

nlp = spacy.load("en_core_web_sm")

print("NER Model Loaded Successfully!")

while True:

    text = input("\nEnter Text (type 'exit' to quit): ").strip()

    if text.lower() == "exit":
        print("\nProgram Closed Successfully!")
        break

    if text == "":
        print("Please enter some text.")
        continue

    doc = nlp(text)

    print("\nNamed Entities")
    print("-" * 40)

    if len(doc.ents) == 0:
        print("No entities found.")

    else:
        for entity in doc.ents:
            print(f"{entity.text} --> {entity.label_}")