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
# Radio button with horizontal layout for ad_type
ad_type = st.radio("Which continent do you want to travel?",
['Americas', 'Australia', 'Europe', 'Asia', 'Africa'], horizontal=True)
#st.write(f"You chose: {ad_type}")

#Once the selection is made the corresponding tourist spots will be display. 
#To upload a csv file which contains all the tourist spots associated with a continent
# Radio button with horizontal layout for ad_platform


# Radio button with horizontal layout for ad_platform
activities = st.radio("What activities do you want?",
['Sightseeing', 'swimming', 'water sports', 'spa', 'Kids theme parks', 'Landmarks', 'Fitness', 'Fashion'], horizontal=True)
#st.write(f"You chose: {ad_platform}")

st.subheader("Budget")

budget = st.slider('How much are you willing to pay per night?', 100, 10000, 200)


# Submit button
if st.button("Submit"):
    st.write("Thank you for submitting the form")
    st.header("Based on selected options the following prompt is created:")
    st.write(f"Consider {ad_type} online advertisements on {ad_platform} for {device_type} with {ad_placement} in {ad_location} for audience interested in {audience_interest}  and ad objective {ad_objective} with bidding strategy {bidding_strategy}. The ad will be aired in {time_of_day} and will be in {language}. The dimension of the ad is {ad_dimensions} and the network where it will be aired is {ad_network}. Can you do a comprehensive research and give me information on how this ad should be?")
    #if st.button("Select this prompt"):
    question_to_answer=f"Consider {ad_type} online advertisements on {ad_platform} for {device_type} with {ad_placement} in {ad_location} for audience interested in {audience_interest}  and ad objective {ad_objective} with bidding strategy {bidding_strategy}. The ad will be aired in {time_of_day} and will be in {language}. The dimension of the ad is {ad_dimensions} and the network where it will be aired is {ad_network}. Can you do a comprehensive research and give me information on how this ad should be?"
    if not openai_api_key:
          st.info("Please add your OpenAI API key")
          st.stop()
    client = OpenAI(api_key=openai_api_key)
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful assistant with extensive experience in advertising, data science and technical writing."},
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


