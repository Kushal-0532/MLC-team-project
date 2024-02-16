import streamlit as st
from Main_sb import main
import calendar
from streamlit_calendar import calendar
from streamlit_lottie import st_lottie
import requests

style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Josefin+Sans:ital,wght@0,100..700;1,100..700&display=swap'); 

h1{
  font-family: 'Josefin Sans', sans-serif;
}
</style>
"""
style2="""
<style>
@import url('https://fonts.googleapis.com/css2?family=Exo+2:ital,wght@0,100..900;1,100..900&display=swap')
</style>
h4{
  font-family: 'Exo_2', sans-serif;
}

"""




st.markdown(style, unsafe_allow_html=True)




# Define pages
def load_lottieurl(url):
    req=requests.get(url)
    if req.status_code!=200:
        return None
    return req.json()


def home():
    st.markdown("<h1>Study Buddy</h1>",unsafe_allow_html=True)

def what_we_do():
    st.markdown("<h1>What We Do</h1>",unsafe_allow_html=True)
    st.markdown("""<h4>In seconds, Study Buddy transforms your dense PDFs into bite-sized personalized questions and answers. No more sifting through paragraphs for key points, no more agonizing over what to study next.</h4>""",unsafe_allow_html=True)
    st.write()
    st.markdown("<h4>\n  But it doesn't stop there. Study Buddy doesn't just answer your questions - it asks brilliant ones too. Our smart Al generates customized quizzes that target your understanding gaps.</h4>", unsafe_allow_html=True)

def focus():
    st.markdown("<h1>Focus ⏲️</h1>",unsafe_allow_html=True)
    st.link_button("Click here to maximise your productivity","https://lifeat.io/app?appMode=focus&space=844")
    lot=load_lottieurl("https://lottie.host/308a5bf4-2b84-463e-8db0-7b6042857dca/ErhCS7auiI.json")
    st_lottie(lot, height=250)

    
def calendarfunct():
    st.markdown("<h1>Calendar 🗓️</h1>",unsafe_allow_html=True)
    cale = calendar()
    st.write(cale)
def cafe():
    st.markdown("<h1>Cafe ☕</h1>",unsafe_allow_html=True)
    st.link_button("Click here to go to cafe","https://imissmycafe.com/")
    lot=load_lottieurl("https://lottie.host/60a2e02f-d2c1-465a-b771-b85630295b67/JwjJb4Etpb.json")
    st_lottie(lot, height=500,key="coding")
        
# Page routing 
page = st.sidebar.selectbox("Page Navigation", ["Study Buddy 📚","What We Do","Calendar 🗓️","Cafe ☕","Focus ⏲️"])


if page == "Study Buddy 📚":
    home()
    main()
elif page == "What We Do":   
    what_we_do()

elif page == "Calendar 🗓️":
    calendarfunct()
elif page == "Cafe ☕":
    cafe()
elif page == "Focus ⏲️":
    focus()

    
# Page styling
st.markdown("""
        <style> 
            div[data-testid="column"] {
                background-image: url("https://img.mit.edu/files/images/202211/MIT-Neural-Networks-SL.gif");
            } 
        </style>
    """, unsafe_allow_html=True)
