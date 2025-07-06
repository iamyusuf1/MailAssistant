import google.generativeai as genai

# Paste your Gemini API key here
genai.configure(api_key="AIzaSyBjqHsN0hjmVNmCiQdiPNsgYzbsihoY3EU")  # Replace with your real key

def summarize_email(subject, body):
    prompt = f"""You are an intelligent assistant. Given the subject and body of an email newsletter, do the following:
1. Summarize the **entire content** clearly.
2. Explain every **AI tool mentioned**, including what it does.
3. Format the output in clean bullet points or sections.

Email Subject: {subject}
Email Body: {body}
"""

    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")  # This is the correct one!
    response = model.generate_content(prompt)

    summary = response.text
    print("\n🤖 Gemini Summary:\n", summary)
    return summary
