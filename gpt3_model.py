import openai
openai.api_key = "your-api-key"

# generate text using GPT-3
prompt = "What is the price of Bitcoin today?"
model = "text-davinci-002"
response = openai.Completion.create(
    engine=model,
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)

# handle the response
if response.choices:
    text = response.choices[0].text
    print(text)
else:
    print("No response received from GPT-3.")
