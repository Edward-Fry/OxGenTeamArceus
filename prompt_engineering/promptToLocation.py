import openai
import json

import prompt_filtering

OPENAI_API_KEY = "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"

PROMPT_MESSAGE = 'Using the above sentence complete the following task, ' \
                 'do not answer until you have fully read and understood the prompt. ' \
                 'All requirements of the prompt must be followed. ' \
                 'Requirement 1: Extract the starting position and ending position of the subject from the sentence. ' \
                 'Requirement 2: Extract all landmarks the subject mentions in the sentence.  ' \
                 'Requirement 3: Extract the object/landmark the subject wants to locate using the context of the sentence and how far along the journey they were when seeing it. For example, if the sentence was: There’s a nice forest with lots of running routes, about a 20 minute drive from Wordsley in the direction of Kidderminster {"starting_position": "Wordsley", "ending_position": "Kidderminster", "landmarks": "["forest", "running routes"]", "time": "20 minute drive", "landmark_of_interest": "forest"} Note how the landmarks were returned as a python list. If a field is not given by the subject just enter "not specified".'
def get_location_predictions(key_prompt_info:str) -> list[str]:

    openai.api_key = OPENAI_API_KEY

    # print(PROMPT_MESSAGE)
    prediction_prompt = open("prediction_prompt.txt", "r").read() #the prompt passed to api
    number_of_generated_sentences_at_once = 1 #number of datapoints generated per call

    completion1 = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": key_prompt_info + "\n" + prediction_prompt}
        ],
        max_tokens=100,
        n=number_of_generated_sentences_at_once
    )

    # create a list of options returned by the api
    api_response = completion1.choices[0].message.content
    possible_matches = []
    if len(api_response) > 10:
        possible_matches = [(" ").join(name.split(' ')[1:]) for name in api_response.split('\n')]

    return possible_matches
    
if __name__ == "__main__":
    test_prompt = "There’s a nice forest with lots of running routes, about a 20 minute drive from Wordsley in the direction of Kidderminster"
    # test_prompt = "After walking out of Oxford station I was walking towards Jesus College, I crossed a bridge with a Canal and greenery, it was about 5 minutes of walking time from the station, what do you think that canal was ?"
    # test_prompt = "I was travelling from London to Oxford on the train and saw some beautiful yellow fields during my journey, do you know where these may be?"
    key_prompt_info = prompt_filtering.extract_key_info_from_prompt(test_prompt)
    print(f"key_prompt_info: {key_prompt_info}")
    print(get_location_predictions(key_prompt_info))
