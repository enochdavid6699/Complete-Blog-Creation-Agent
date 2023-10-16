# Imports
import requests
import os
from dotenv import load_dotenv
import openai

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")


# Creating Post topics by provided category with manual approval

def generate_topic(category):
    while True:
        prompt = f"Generate a topic related to the category: {category}"
        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,  # You can adjust the max_tokens as needed
            n=3,            # You can adjust n as needed to get multiple suggestions
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
category = input('Enter a Category: ')


approved_topics = generate_topic(category)
print(f"Approved Topic: {approved_topics}")


# Creating blogs for approved topics
def generate_blog_content(topic):
    prompt = f"Write a blog post on the following topic: {topic}"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,  # You can adjust the max_tokens as needed for the length of the blog
    )
    
    blog_content = response.choices[0].text.strip()
    
    return blog_content

def approve_blog(blog_content):
    print("--- Blog Topic ---")
    print(topic)
    print("\n")
    print("--- Blog Content ---")
    print(blog_content)
    print("\n")
    approval = input("Do you approve this blog? (y/n): ").strip().lower()
    
    if approval == 'y': 
        return 'y'
    else:
        return 
        

# Generate and review blogs for approved topics
approved_blogs = {}
for topic in approved_topics:
    
    while True:
        blog_content = generate_blog_content(topic)
        if approve_blog(blog_content):
            approved_blogs[topic] = blog_content
            break
        else: 
            blog_content = generate_blog_content(topic)
        

# Print or save the approved blogs
for topic, content in approved_blogs.items():
    print(f"--- Approved Blog for {topic} ---")
    print(content)
    print("\n")

