# importing libraries
import streamlit as st
import requests

base_url = "http://127.0.0.1:4000/"

# configuring the page
st.set_page_config(page_title='OList Store', layout='centered', initial_sidebar_state='auto')

# getting the json response from the api
def recommend(in_user):
    resp = requests.get(base_url + "recommend/" + str(in_user))
    return resp.json()

# customizing the ui of the app
def main():
    st.markdown("<h1 style='text-align: center; color: white;'>OList Store</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: white;'>Welcome to our Store!</h2>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: white;'>Please login to continue!</h3>", unsafe_allow_html=True)
    in_user = st.text_input('Enter UserID: ')
    login = st.button(label='Login')

    if login:
        st.markdown("<h3 style='text-align: center; color: white;'>Here are some recommendations for you!</h3>", unsafe_allow_html=True)
        prods = recommend(in_user)
        if 'details' not in prods: 
            for p in prods:
                st.write(p)

    st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: white;'>Have a look at our top products!</h3>", unsafe_allow_html=True)
    prods = recommend('0000')
    if 'details' not in prods: 
        for p in prods:
            st.write(p)
  
  
if __name__ == '__main__':
    main()
