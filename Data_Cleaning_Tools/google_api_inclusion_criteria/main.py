import os
import pandas as pd
import time
from google import genai

# Set your API key.
API_KEY = os.environ.get('GOOGLE_GENAI_API_KEY')
client = genai.Client(api_key=API_KEY)

def classify_article(title):
    """
    Uses the generate_content endpoint to classify an article title as
    "Relevant" if it meets the inclusion criteria; otherwise, returns "Irrelevant".
    """
    prompt = (
        f"Determine if the following article title meets these criteria:\n\n"
        "1. It addresses clinical research/clinical trials and/or Digital Health Technologies.\n"
        "2. It discusses barriers or strategies around DEI (Diversity, Equity, and Inclusion).\n\n"
        "Reply with exactly one word: either 'Relevant' or 'Irrelevant'.\n\n"
        f"Article Title: \"{title}\""
    )
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        answer = response.text.strip()
        # Enforce expected output; if not exactly matching, default to "Irrelevant"
        if answer not in ["Relevant", "Irrelevant"]:
            answer = "answer.error"
        return answer
    except Exception as e:
        print(f"Error processing title '{title}': {e}")
        return "exception.error"

def generate_explanation(title):
    """
    Generates an explanation of why the article title is not relevant.
    This function is called only when the classification is 'Irrelevant'.
    """
    explanation_prompt = (
        "Explain why the following article title is not relevant to clinical research/clinical trials, "
        "Digital Health Technologies, or discussions about DEI (Diversity, Equity, and Inclusion):\n\n"
        f"Article Title: \"{title}\""
    )
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=explanation_prompt
        )
        explanation = response.text.strip()
        return explanation
    except Exception as e:
        print(f"Error generating explanation for title '{title}': {e}")
        return "No explanation available"

def main():
    # Load the CSV file containing the "Article Title" column.
    input_filename = "C:/Users/Pixel/PycharmProjects/IEEE_QualSyst/Databases/search_and_scrape_data/filtering_training_data_10.csv"
    df = pd.read_csv(input_filename)

    if "Article Title" not in df.columns:
        raise ValueError("CSV file must contain an 'Article Title' column.")

    results = []
    explanations = []
    for title in df["Article Title"]:
        result = classify_article(title)
        # If the classification is "Irrelevant", generate an explanation.
        if result == "Irrelevant":
            explanation = generate_explanation(title)
        else:
            explanation = ""  # Optionally leave empty or set to "N/A" for relevant titles.
        results.append(result)
        explanations.append(explanation)
        # Pause briefly to respect API rate limits.
        time.sleep(1)

    # Append the new columns to the dataframe.
    df["Result"] = results
    df["Explanation"] = explanations

    # Save the updated dataframe to a new CSV file.
    output_filename = "output.csv"
    df.to_csv(output_filename, index=False)
    print(f"Results saved to {output_filename}")

if __name__ == "__main__":
    main()
