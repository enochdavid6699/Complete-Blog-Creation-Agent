#Imort statements
import requests
import os
from dotenv import load_dotenv
import openai

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables
# api_endpoint = os.getenv("API_ENDPOINT")
# api_key = os.getenv("API_KEY")
# api_secret = os.getenv("API_SECRET")
openai.api_key = os.getenv("OPENAI_API_KEY")



# Creating Post topics by provided category with manual approval

def generate_topic(category):
    while True:
        prompt = f"Generate a topic related to the category: {category}"
        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,  # You can adjust the max_tokens as needed
            n=5,            # You can adjust n as needed to get multiple suggestions
            stop=None
        )
        
        topics = [choice.text.strip() for choice in response.choices]
        
        for i, topic in enumerate(topics, start=1):
            print(f"Generated Topic {i}:\n{topic}\n")
        
        approval = input("Do you approve any of these topics? Enter the number(s) of the topic(s) you approve (e.g., '1 3'), or 'n' to generate a new topic: or 'y' if you want to approve all topics: ").strip().lower()
        if approval == 'n':
            print("Generating a new topic...\n")
        elif approval == 'y':
            approved_topics = topics
            return approved_topics
        else:
            approved_topics = [topics[int(index) - 1] for index in approval.split()]
            return approved_topics

# Input your desired category here
category = "Technology"

approved_topic = generate_topic(category)
print(f"Approved Topic: {approved_topic}")


# Creating blogs for approved topics
# def generate_blog_content(topic):
#     prompt = f"Write a blog post on the following topic: {topic}"
    
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=500,  # You can adjust the max_tokens as needed for the length of the blog
#     )
    
#     blog_content = response.choices[0].text.strip()
    
#     return blog_content

# Generate blogs for approved topics
# blog_posts = {}
# for i, topic in enumerate(approved_topics, start=1):
#     print(f"Generating blog for Approved Topic {i}: {topic}")
#     blog_content = generate_blog_content(topic)
#     blog_posts[topic] = blog_content

# Print or save the generated blogs
# for topic, content in blog_posts.items():
#     print(f"--- Blog Post for {topic} ---")
#     print(content)
#     print("\n")


# Posting on wordpress

# Create the post data (customize this to your needs)
# post_data = {
#     'title': 'Your Daily Blog Post Title',
#     'content': 'Your blog post content goes here.',
#     'status': 'publish',
# }

# Set up the request headers with basic authentication
# headers = {
#     'Authorization': 'Basic ' + base64.b64encode(f'{api_key}:{api_secret}'.encode()).decode(),
#     'Content-Type': 'application/json',
# }

# Send the POST request to create the post
# response = requests.post(api_endpoint, json=post_data, headers=headers)

# if response.status_code == 201:
#     print('Post created successfully.')
# else:
#     print('Error:', response.status_code, response.text)
