import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# Ensure set_page_config is called first
st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")

# Add custom CSS for background color and image
def add_background_image(image_url, color):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-color: {color};
        }}
        h1 {{
            color: yellow;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="", placeholder="Enter the job posting URL here")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            # Removed portfolio.load_portfolio() as it doesn't exist
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.generate_cold_email(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    # Set the background image and color
    add_background_image("https://cdn.prod.website-files.com/64ac5313fdc3db427c2f5512/653687e136dce583259e85bb_Hard%20Bounce%20vs.%20Soft%20Bounce%20Emails%20What%27s%20the%20Difference%20(9)-min.jpg", "#f0f0f0")
    
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
