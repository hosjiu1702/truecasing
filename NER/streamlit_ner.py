import streamlit as st
from annotated_text import annotated_text
from ner import *
import requests

def find_index_entity(start_index,source_string,target_entity):
    '''
    Function for processing data, convert raw data to numeric data
    Input:
        start_index: start index of the entity in the string
        source_string: string to find entity
        target_entity: Tag
    Output:
        end_index: end index of the entity in the string
        entity_name: name of entity is contained in input string
    '''
    entity_name = target_entity.split('-')[1]
    find_value = 'I-'+ entity_name
    end_index = start_index
    if (start_index == len(source_string)-1):
        end_index = start_index
    else:
        i = start_index +1
        while(i<len(source_string)):
            if(source_string[i] == find_value):
                end_index = i
                i+=1
            else:
                break
    return end_index, entity_name


dict_color = {'SYS.STREET_NUMBER': "#8ef", 'SYS.STREET': "#faa",
'SYS.DISTRICT': "#afa",'SYS.CITY': '#bca',  'SYS.WARD': "#fea",
'SYS.ADDRESS_LAND': "#8ef", 'SYS.ADDRESS_HAMLET': "#aaf",
'SYS.ADDRESS_VILLAGE': '#e8f', 'SYS.QUARTER': '#abc',
'SYS.ADDRESS_GROUP': '#bca', 'SYS.ADDRESS_LANE': '#cba', 'SYS.TOWN': '#a32', 
'SYS.ADDRESS_APARTMENT': '#456',  'SYS.URBAN_AREA': '#435',
'SYS.FLOOR': '#bca', 'SYS.ADDRESS_ROOM': '#bca',  'SYS.ADDRESS_ALLEY': '#faa',
'SYS.LICENSE_PLATE_NUMBER': '#afa','SYS.FULL_NAME': '#8ef',
}

df = load_data('data/data_ner.xlsx')
path = 'model.hdf5'

word2idx, tag2idx, idx2word, idx2tag, num_tag,words, tags = process_data(df)
model =  load_model(num_tag, words, path)


# New model
st.title("DEMO NAME ENTITY RECOGNITION")
#Textbox for text user is entering
st.subheader("Please enter your text")
text = st.text_input('Enter text') #text is stored in this variable
text = text.lower()
st.header("New Model")
if (len(text)>0):
    text_ws =[]
    text_ws.append(text.split(' '))
    tag = ner_inference(text_ws, model, word2idx, idx2tag)
    #Display results of the NLP task

    display = []
    for i in range(len(tag)):
        j = 0
        while(j <len(tag[i])):
            if (tag[i][j]=='O'):
                display.append(' '.join(text_ws[i][j].split('_'))+" ")
                j+=1
            else:
                end_index,entity = find_index_entity(j,tag[i],tag[i][j])
                value_tag = tag[i][j].split('-')[1]
                display.append((' '.join(('_'.join(text_ws[i][j:end_index+1])).split('_'))+" ",value_tag,dict_color[value_tag]))
                j = end_index+1

    annotated_text(*display)


# Old model
st.header("Old Model")
text_ws_old =[] 
text_ws_old.append(text.split(' '))
#Display results of the NLP task

url = 'https://ge-dev.vnlp.ai/api/v2/entity'
headers = {'Authorization': 'bW=bD&X8+@gcJCmMxCmZY?6p*JGCrc#7'}
data_ = {'data': [text]}
tag_old =  requests.post(url, headers=headers, json=data_).json()
display_old = []
if 'sys.full_name' in tag_old[0].keys():
    slice = [0]
    for i in tag_old[0]['sys.full_name']:
        slice.append(i['begin'])
        slice.append(i['end'])
    slice.append(len(text))
    for i in range(len(slice)-1):
        if i%2==0:
            display_old.append(text[slice[i]:slice[i+1]])
        else:
            display_old.append((text[slice[i]:slice[i+1]],'SYS.FULL_NAME',dict_color['SYS.FULL_NAME']))

else:
    display_old.append(text)

annotated_text(*display_old)
