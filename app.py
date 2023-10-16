# Imports
import os
from dotenv import load_dotenv
import openai
import streamlit as st

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
        
        st.write("Generated Topics:")
        for i, topic in enumerate(topics, start=1):
            st.write(f"Generated Topic {i}:\n{topic}\n")
        
        approval = st.text_input("Do you approve any of these topics? Enter the number(s) of the topic(s) you approve (e.g., '1 3'), 'n' to generate a new topic, or 'y' if you want to approve all topics:")
        if approval == 'n':
            st.write("Generating a new topic...\n")
        elif approval == 'y':
            approved_topics = topics
            return approved_topics
        else:
            approved_topics = [topics[int(index) - 1] for index in approval.split()]
            return approved_topics

# Input your desired category here
st.title('Blog Topic Generation')
category = st.text_input('Enter a Category:')

approved_topics = None  # Initialize approved_topics as None

if category:
    approved_topics = generate_topic(category)
    st.write(f"Approved Topics: {approved_topics}")

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

def approve_blog(blog_content, topic):
    st.write("--- Blog Topic ---")
    st.write(topic)
    st.write("\n")
    st.write("--- Blog Content ---")
    st.write(blog_content)
    st.write("\n")
    # Generate a unique key based on the topic
    key = f"approval_{topic.replace(' ', '_')}"
    approval = st.radio("Do you approve this blog?", ('Yes', 'No'), key=key)
    
    return approval

# Generate and review blogs for approved topics
if approved_topics:
    approved_blogs = {}
    for topic in approved_topics:
        while True:
            blog_content = generate_blog_content(topic)
            user_approval = approve_blog(blog_content, topic)
            if user_approval == 'Yes':
                approved_blogs[topic] = blog_content
                break
            else: 
                blog_content = generate_blog_content(topic)

    # Print or save the approved blogs
    for topic, content in approved_blogs.items():
        st.write(f"--- Approved Blog for {topic} ---")
        st.write(content)
        st.write("\n")

