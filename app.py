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
ad_type = st.radio("Which continent do you want to travel?"),
['Americas', 'Australia', 'Europe', 'Asia', 'Africa'], horizontal=True)
#st.write(f"You chose: {ad_type}")

#Once the selection is made the corresponding tourist spots will be display
# Radio button with horizontal layout for ad_platform
ad_platform = st.radio("What Ad platform do you want?",
['Facebook', 'Google', 'Instagram', 'LinkedIn'], horizontal=True)
#st.write(f"You chose: {ad_platform}")

# Radio button with horizontal layout for ad_platform
device_type = st.radio("What device type do you want?",
['Mobile', 'Laptop', 'Tablet'], horizontal=True)
#st.write(f"You chose: {ad_platform}")


# Radio button with horizontal layout for ad_platform
ad_placement = st.radio("What ad placement do you want?",
['Banner', 'Sidebar', 'Pre-roll', 'Pop-up', 'In-feed','Sponsored content'], horizontal=True)
#st.write(f"You chose: {ad_platform}")


# Radio button with horizontal layout for ad_platform
ad_location = st.radio("What ad location do you want?",
['Upper Left', 'Lower Left', 'Upper right', 'Lower right', 'Center','Upper Centre', 'Lower Centre'], horizontal=True)
#st.write(f"You chose: {ad_platform}")


st.subheader("Target Audience")

age = st.slider('What age are you targetting?', 0, 100, 25)

gender = st.radio(
    "What gender are you targetting?",
    ('Male', 'Female', 'Non-binary'))

income = st.slider('What income range are you targetting?', 0, 100000, 50000)

location = st.text_input('What location are you targetting?')

audience_interest = st.radio("What audience interest are you targetting?",
['Technology', 'Fitness', 'Travel', 'Fashion', 'Movies'], horizontal=True)
#st.write(f"You chose: {ad_platform}")

ad_objective = st.radio("What audience interest are you targetting?",
['Brand Awareness', 'Lead generation', 'App installs', 'Sales conversion'], horizontal=True)

bidding_strategy = st.radio("What is your bidding strategy?",
['Cost per click', 'Cost per thousand impressions', 'Cost per acquisition'], horizontal=True)


language = st.radio("What is ad language?",
['English', 'Spanish','Hindi', 'Mandarin', 'French'], horizontal=True)


time_of_day = st.radio("What time of the day do you want?",
['Morning', 'Afternoon','Evening', 'Night'], horizontal=True)


ad_dimensions = st.radio("Dimensions of the ad?",
['300X250', '728X90','160X600'], horizontal=True)


ad_network = st.radio("What is the ad network",
['Google Display Network', 'Facebook audience network', 'Adsense'], horizontal=True)

#def generate_response(input_text):
  # model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
    #st.info(model.invoke(input_text))


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


