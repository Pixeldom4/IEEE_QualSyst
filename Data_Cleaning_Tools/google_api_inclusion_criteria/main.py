import pandas as pd
import time
from google import genai
from google.genai import types

# Initialize the client with your API key.
client = genai.Client(api_key="YOUR_API_KEY")


def classify_article(title):
    """
    Uses the generative AI chat endpoint to classify an article title as
    "Relevant" if it addresses clinical research/trials and/or digital health or
    DEI-related barriers/strategies; otherwise, returns "Irrelevant".
    """
    prompt = (
        f"Determine if the following article title meets these criteria:\n\n"
        "1. It addresses clinical research/clinical trials and/or Digital Health Technologies.\n"
        "2. It discusses barriers or strategies around DEI (Diversity, Equity, and Inclusion).\n\n"
        "Reply with exactly one word: either 'Relevant' or 'Irrelevant'.\n\n"
        f"Article Title: \"{title}\""
    )

    try:
        response = client.chat(
            messages=[types.Message(content=prompt, author=types.Author.USER)],
            model="models/chat-bison-001"  # Update model name if necessary.
        )
        # Assuming the response returns a 'last_message' with a 'text' attribute.
        answer = response.last_message.text.strip()
        # Enforce expected output; if not exactly matching, default to Irrelevant.
        if answer not in ["Relevant", "Irrelevant"]:
            answer = "Irrelevant"
        return answer
    except Exception as e:
        print(f"Error processing title '{title}': {e}")
        return "Irrelevant"


def main():
    # Load the CSV file containing the "Article Title" column.
    input_filename = "C:/Users/Pixel/PycharmProjects/IEEE_QualSyst/Databases/search_and_scrape_data/filtering_training_data_5000.csv"
    df = pd.read_csv(input_filename)

    if "Article Title" not in df.columns:
        raise ValueError("CSV file must contain an 'Article Title' column.")

    results = []
    for title in df["Article Title"]:
        result = classify_article(title)
        results.append(result)
        # Pause briefly to respect API rate limits.
        time.sleep(1)

    # Add a new column with the classification results.
    df["Result"] = results

    # Save the updated dataframe to a new CSV file.
    output_filename = "output.csv"
    df.to_csv(output_filename, index=False)
    print(f"Results saved to {output_filename}")


if __name__ == "__main__":
    main()
