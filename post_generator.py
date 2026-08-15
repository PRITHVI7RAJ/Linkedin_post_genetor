from http.client import responses

from pymsgbox import prompt

from llm_helper import llm
from few_shot import FewshortPosts

few_shot = FewshortPosts()

def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 15 lines"
    if length == "Long":
        return "15 to 35 lines"

def get_prompt (length ,language, tag):
    length_str = get_length_str((length))
    prompt = f'''
    Generate a LinkedIn post using the below information . No preamble.
    
    1) Topic :{tag}
    2) Length : {length}
    3) Language : {language}
    if language is Hinglish then it means it is a mix of Hindi and English.
    The script for the generated post should always be English.
'''
    example =few_shot.get_filtered_posts(length ,language, tag)

    if len(example)>0:
        prompt +="4) use the writing style as per the following example."
        for i , post in enumerate(example):
            post_text = post['text']
            prompt += f"\n\n Example {i+1}: \n\n {post_text}"
            if i== 1:
                break
    return prompt

def generate_post(length ,language, tag):
    prompt = get_prompt(length ,language, tag)
    response = llm.invoke(prompt)
    return response.content

if __name__=="__main__":
    #post = get_prompt("Medium", "Hinglish","jobseekers")
    post = generate_post("Medium", "Hinglish", "jobseekers")
    print(post)
