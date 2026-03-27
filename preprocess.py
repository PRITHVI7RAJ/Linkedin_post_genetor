import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from langchain_core.exceptions import  OutputParserException
from llm_helper import llm


def process_posts(raw_file_path,processed_file_path="data/processed_posts.json"):
    enriched_posts = []
    with open(raw_file_path,encoding='utf-8') as file:
      posts = json.load(file)
      for post in posts:
          metadata= extract_metadata(post['text'])
          post_with_metadata = post | metadata
          enriched_posts.append(post_with_metadata)

    unified_tags = get_unified_tags(enriched_posts)

    for post in enriched_posts:
        current_tags = post['tags']
        new_tags = {unified_tags[tag] for tag in current_tags}
        post['tags'] = list(new_tags)

    with open(processed_file_path,encoding='utf-8',mode="w") as outfile:
        json.dump(enriched_posts, outfile,indent=4)




def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])

    return {tag: tag for tag in unique_tags}

    unique_tags_list = ','.join(unique_tags)

def extract_metadata(post):
    template = '''
    You are given a LinkedIn post.You need to extract number of lines, Language of the post and tags.
     1. Return a valid JSON. No preamble.
     2. JSON object should have exactly three keys: line_count, language and tags.
     3. tags is an array of text tags. Extract maximum two tags.
     4. Language should be English or HingLish (Hinglish means hindi + english)
      Here is the actual post on which you need to perform this task:
      {post_abc}
       '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm # | means AND   # chain means u supply above template prompt to llm
    response = chain.invoke(input = {'post_abc':post})

    try:
       json_parser = JsonOutputParser()
       res= json_parser.parse(response.content)
    except OutputParserException:
           raise  OutputParserException("context too big . unable to parse jobs")
    return res

if __name__== "__main__":
    process_posts("data/raw_posts.json","data/processed_posts.json")