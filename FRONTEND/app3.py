import streamlit as st
import wikipedia
import folium
from streamlit_folium import st_folium
import requests
from requests import session
page_bg_img=""" <style> [data-testid="stAppViewContainer"]{
background: rgb(252,100,132);
background: linear-gradient(157deg, rgba(252,100,132,1) 0%, rgba(82,56,170,1) 100%);}
[data-testid="stHeader"]{
    background-color: rgba(0,0,0,0);
    right: 4rem;
}
[data-testid="stSidebar"]{
    background: rgb(34,193,195);
background: linear-gradient(0deg, rgba(34,193,195,1) 0%, rgba(253,187,45,1) 100%);

}

</style>"""
st.markdown(page_bg_img,unsafe_allow_html=True)
st.sidebar.header("WELCOME TO TEST SERVER")
st.caption("")
st.markdown('''<h4 style='text-align: left;color: #31333F; font-weight:bold;'>Data set of 450 bird species. 70,626 training images, 22500 test images(5 images per species) and 2250 validation images(5 images per species. This is a very high quality dataset where there is only one bird in each image and the bird typically takes up at least 50% of the pixels in the image. As a result even a moderately complex model will achieve training and test accuracies in the mid 90% range.
    All images are 224 X 224 X 3 color images in jpg format. Data set includes a train set, test set and validation set. Each set contains 450 sub directories, one for each bird species. The data structure is convenient if you use the Keras ImageDataGenerator.''',unsafe_allow_html=True)

st.markdown('''<h4 style='text-align: left;color: #31333F; font-weight:bold;'>Because of the large size of the dataset I recommend if you try to train a model use and image size of 150 X 150 X 3 in order to reduce training time. All files were also numbered sequential starting from one for each species. So test images are named 1.jpg to 5.jpg. Similarly for validation images. Training images are also numbered sequentially with "zeros" padding. For example 001.jpg, 002.jpg ….010.jpg, 011.jpg …..099.jpg, 100jpg, 102.jpg etc. The zero's padding preserves the file order when used with python file functions and Keras flow from directory.
The training set is not balanced, having a varying number of files per species. However each species has at least 130 training image files.
''',unsafe_allow_html=True)
st.markdown('''<h4 style='text-align: left;color: #31333F; font-weight:bold;'>One significant shortcoming in the data set is the ratio of male species images to female species images. About 80% of the images are of the male and 20% of the female. Males typical are far more diversely colored while the females of a species are typically bland. Consequently male and female images may look entirely different .Almost all test and validation images are taken from the male of the species. Consequently the classifier may not perform as well on female specie images.''',unsafe_allow_html=True)  
  


st.markdown('''<h4 style='text-align: left;color: #31333F; font-weight:bold;'> First of all we selected MobileNet from various models like VGG16, AlexNet, GoogleNet because of its low latency, low complexity and most importantly less training time.''',unsafe_allow_html=True)
st.markdown('''<h4 style='text-align: left;color: #31333F; font-weight:bold;'> We have selected last 20 layer from 28 total layers. Then we augmented the data using the keras ImageDataGenerator. We have used adam optimizer and categorical crossentropy  and accuracy as performance matrix.''',unsafe_allow_html=True)

st.markdown('''<h4 style='text-align: left;color: #31333F; font-weight:bold;'>After setting the epoch size to 64 and batch size to 64 and steps per epochs to len(train_data), we were able to reduce the training time of the model from 12-15 hours to 3-5 hours at the cost of 2% accuracy.''',unsafe_allow_html=True)
st.markdown('''<h4 style='text-align: left;color: #31333F; font-weight:bold;'>later we tested our model on several different bird species and every time.''',unsafe_allow_html=True)
X=wikipedia.summary('CRANE HAWK',6)
st.markdown('''<h4 style=text-align:left;font-weight:bold;color:#31333F;'>-----------------------------------------------------------------------------Description of the given bird:''',unsafe_allow_html=True)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)
st.markdown(X)
json_data={}
N='CRANE HAWK'
r = requests.get('https://api.ebird.org/v2/ref/taxon/find?locale=en_US&cat=species&key=jfekjedvescr&q='+N,data = json_data) 
R=r.json()
info_dic=(R[0])
code_name=([value for value in info_dic.values()][0])# fetching the code name of the bird
from requests import Session
session = Session()
url  ="https://api.ebird.org/v2/data/nearest/geo/recent/{}?lat={}&lng={}&maxResults=10"
headers = {"x-ebirdapitoken" : "s9hfc8f0grqs"}
full_info=(session.get(url.format(code_name, "0", "0"), headers=headers).text) # fetching the details of the bird using the codename
import json
Result = json.loads(full_info)
coor=( [ (value["lat"], value["lng"]) for value in Result ] )
coor2=list(coor[1])
map=folium.Map(location=coor2,zoom_start=5,tiles='Stamen Terrain',scrollWheelMap=False)
# birdicon=folium.features.CustomIcon('bird-icon.jpg',icon_size=(100,100))
for coord in coor:
    folium.Marker(location=coord,popup=N+" is commonly found here",tooltip='Click here to see info',icon=folium.Icon(color="red", icon="asterisk")).add_to(map)
    

st_map=st_folium(map,width=700,height=450,returned_objects=[])
