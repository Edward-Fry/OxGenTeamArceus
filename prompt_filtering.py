import openai

OPENAI_API_KEY = "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"
def extract_key_info_from_prompt(prompt:str) -> str:

    openai.api_key = OPENAI_API_KEY

    prompt1 = open("prompt_message.txt", "r").read() #the prompt passed to api
    number_of_generated_sentences_at_once = 1 #number of datapoints generated per call

    #first call
    completion1 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt + "\n" + prompt1}
        ],
        max_tokens=100,
        n=number_of_generated_sentences_at_once
    )

    return completion1.choices[0].message.content


if __name__ == "__main__":
    # input = "hi i was cycling in a park in london and happened to pass by a really beautiful chinese style building. it had a green roof and red pillars next to a wide red path. i happened to pass by a flower garden on my way there. would you know where this is?"
    input = "There’s a nice forest with lots of running routes, about a 20 minute drive from Wordsley in the direction of Kidderminster"
    extract_key_info_from_prompt(input)
