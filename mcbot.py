# McBot
import pandas as pd
import numpy as np
import aiml, os
from streamlit_chat import message
import streamlit as st 
from PIL import Image

id_sessi = "123456"

# ambil data dari csv
df = pd.read_csv("mcd.csv")
df.fillna(0, inplace=True)
df.replace(to_replace = np.nan, value = 0)
promos = df[df["R/L"]==1]

# fungsi fitur
def tunjukkan_promo():
    promo =""
    for i in range(len(promos)):        
        harga = str(int(promos.iloc[i,3]))
        if promos.iloc[i,3]== 0.0:     
            harga = str(int(promos.iloc[i,4]))
            if promos.iloc[i,4] == 0.0:
                harga = str(int(promos.iloc[i,2]))            
        promo += "\n"+promos.iloc[i,1]+ " Rp "+harga+", "
    return promo

def tunjukkan_item():
    response=""
    cari = kern.getPredicate("item", id_sessi)    
    for i in range(len(df)):
        if cari.title() in df["Nama"][i] or cari in df["Nama"][i]:
            response += df["Nama"][i]
            if int(df.iloc[i,2])!=0:
                response += " A-la-Carte Rp "+str(int(df.iloc[i,2]))+","
            if int(df.iloc[i,3])!=0:
                response += " dengan Paket Nasi Rp "+str(int(df.iloc[i,3]))+","
            if int(df.iloc[i,4])!=0:
                response += " & dengan Paket Fries Rp "+str(int(df.iloc[i,4]))                                 
            response += "\n"
    kern.setPredicate("reply",response,id_sessi)  

#inisialisasi bot
kern = aiml.Kernel()
kern.setPredicate("promo",tunjukkan_promo(),id_sessi)
BOT_SESSION_PATH = "/py/coba/"
if os.path.isfile("bot_brain.brn"):
        kern.bootstrap(brainFile = "bot_brain.brn", commands = "MCBOT")
else:
    kern.bootstrap(learnFiles = "McBot.xml", commands = "MCBOT")
    kern.saveBrain("bot_brain.brn")        

#UI
img = Image.open('McD.png')
st.set_page_config(
    page_title="McBot",
    page_icon=img
)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

chat = st.empty()    

#UI Display Chat + Input processing
user_input = st.text_input("You: ","")
if user_input: 
    output = kern.respond(user_input,id_sessi)    
    if output:        
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)
    elif output == "":
        tunjukkan_item() 
        output2 = kern.respond(user_input,id_sessi)
        if output2:        
            st.session_state.past.append(user_input)
            st.session_state.generated.append(output2)
        elif output2 == "":
            st.session_state.past.append(user_input)
            st.session_state.generated.append("Maaf input tidak dimengerti. Mohon diulangi")

with chat.container():
    message("Selamat Datang di McBot demo")        
    if st.session_state['generated']:
        for i in range(0,len(st.session_state['generated']),1):                      
            message(st.session_state['past'][i], is_user=True, key=str(i)+ '_user',avatar_style="adventurer")
            message(st.session_state["generated"][i],key=str(i), )    