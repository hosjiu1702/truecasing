import streamlit as st
from annotated_text import annotated_text
from ner import ner


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
st.title("DEMO NAME ENTITY RECOGNITION")
#Textbox for text user is entering
st.subheader("Please enter your text")
text = st.text_input('Enter text') #text is stored in this variable
st.header("Results of New Model")
text_ws =[]
text_ws.append(text.split(' '))
tag = ner(text_ws)
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


# st.header("Results of Old Model")
# text_ws_old =[]
# text_ws_old.append(text.split(' '))
# tag_old = ner(text_ws_old)
# #Display results of the NLP task

# display_old = []
# for i in range(len(tag_old)):
#     j = 0
#     while(j <len(tag_old[i])):
#         if (tag_old[i][j]=='O'):
#             display_old.append(' '.join(text_ws_old[i][j].split('_'))+" ")
#             j+=1
#         else:
#             end_index_old,entity_old = find_index_entity(j,tag_old[i],tag_old[i][j])
#             value_tag_old = tag_old[i][j].split('-')[1]
#             display_old.append((' '.join(('_'.join(text_ws_old[i][j:end_index_old+1])).split('_'))+" ",value_tag_old,dict_color[value_tag_old]))
#             j = end_index_old+1

# annotated_text(*display_old)

