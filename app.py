#%%writefile app.py

import streamlit as st
from openai import OpenAI

#from langchain_openai.chat_models import ChatOpenAI

with st.sidebar:
  openai_api_key = st.text_input ("OpenAI API Key", type="password")

st.title("Travel AARK: Planning trip made easier")
st.header("A streamlit chatbot powered by OpenAI:")
st.image("world_map.png")

st.subheader("Please select your options")
# Radio button with horizontal layout for continent
continent = st.radio("Which continent do you want to travel?",
['Americas', 'Australia', 'Europe', 'Asia', 'Africa'], horizontal=True)

# Radio button with horizontal layout for activities
st.write('Select your favorite activities')
activity1 = st.checkbox('sightseeing')
activity2 = st.checkbox('swimming')
activity3 = st.checkbox('water sports')
activity4 = st.checkbox('spa')
activity5 = st.checkbox('Kids theme park')
activity6 = st.checkbox('hiking')
activity7 = st.checkbox('fitness')
activities = activity1 + activity2 + activity3 + activity4 + activity5 + activity6 +activity7

#activities = st.radio("What activities do you want?",
#['Sightseeing', 'swimming', 'water sports', 'spa', 'Kids theme parks', 'Hiking', 'Fitness', 'Fashion'], horizontal=True)

st.subheader("Budget")

budget = st.slider('How much are you willing to pay per night?', 100, 1000, 0)

st.subheader("Days")

days = st.slider('How many days do you want to stay?', 0, 20, 0)

# add a rag 

# Submit button
if st.button("Submit"):
    st.write("Thank you for submitting the form")
    st.header("Based on selected options the following prompt is created:")
    st.write(f"Consider tourist places in {continent}. List the hotels with a budget of  ${budget} per night. List the places to acoomodate the activities such as {activities} for each of the {days} days")
    #if st.button("Select this prompt"):
    question_to_answer=(f"Consider tourist places in {continent}. List the hotels with a budget of  ${budget} per night. List the places to acoomodate the activities such as  {activities}")
    #if st.button("Select this prompt"):
    if not openai_api_key:
          st.info("Please add your OpenAI API key")
          st.stop()
    client = OpenAI(api_key=openai_api_key)
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are aa helpful travel agent with extensive experience in building travel packages for clients"},
        {"role": "user", "content": question_to_answer}])
    st.markdown(completion.choices[0].message.content)


if "messages" not in st.session_state:
 st.session_state["messages"] = [{"role": "assistant", "content": "Is there anything else I can help you with?"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


if prompt := st.chat_input():
  if not openai_api_key:
    st.info("Please add your OpenAI API key")
    st.stop()
  client = OpenAI(api_key=openai_api_key)
  st.session_state.messages.append ({"role": "user", "content": prompt})
  st.chat_message("user").write(prompt)
  response = client.chat.completions.create(messages=st.session_state.messages, model="gpt-3.5-turbo")
  msg = response. choices[0] .message.content
  st.session_state.messages.append ({"role": "user", "content": prompt})
  st.chat_message("assistant").write(msg)


