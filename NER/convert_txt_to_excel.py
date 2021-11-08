import re
import pandas as pd

location = "data/test.txt"
sentences = []
tags = []
words = []
index = 1

def entity_label(entity_label):
    entity = []
    label = []
    entity_label_ = entity_label.split(';')
    for i in entity_label_:
        entity.append(i.split('|')[0])
        label.append(i.split('|')[1])
    return entity, label

def join_entity (entity):
    for i in range(len(entity)):
         entity[i] = '_'.join(entity[i].split(' '))
    return entity

def process_sentence(sentence,entity):
    for i in range(len(entity)):
        sentence = sentence.replace(entity[i], '_'.join(entity[i].split(' ')))
        entity[i]='_'.join(entity[i].split(' '))
    sentence = re.sub(",", " ,", sentence)
    sentence =sentence.split(' ')
    return sentence

def find_tag (sentence, entity, label): 
    tags = []
    for i in sentence:
        if i not in entity:
            tags.append('O')
        else:
            ind = entity.index(i)
            tmp = len(i.split('_'))
            if tmp ==1:
                tags.append('B-'+ label[ind].upper())
            else:
                tags.append('B-'+ label[ind].upper())
                # tags.append(['I-'+ label[ind].upper()]*(tmp-1))
                for j in range(tmp-1):
                    tags.append('I-'+ label[ind].upper())
    return tags

with open(location, 'r',encoding='utf8') as f:
    data = f.readlines() 


for line in data:
    if len(line)>1:
        splitted_line = line.split('\t')
        sentence = splitted_line[0]
        splitted_sentence = re.sub(",", " ,", sentence)
        splitted_sentence =splitted_sentence.split(' ')	

        entity = splitted_line[2][0:len(splitted_line[2])-1]
        entity, label = entity_label(entity)

        joined_sentence = process_sentence(sentence,entity)
        # print(entity)
        # print(joined_sentence)
        # print(label)
        # print('...............................')

        entity = join_entity(entity)
        tag = find_tag (joined_sentence,entity, label)
        if (len(tag) != len(splitted_sentence)):
            # print(len(tag), len(splitted_sentence))
            # print(tags)
            # print(splitted_sentence)
            print(line)
            # print('...............................')

        sentences.extend([index]*len(tag))
        tags.extend(tag)
        words.extend(splitted_sentence)
        index +=1
        # if index ==5:break
        

print(len(words))
print(len(tags))
print(len(words))



    
frame = {'sentence':sentences,'word':words,'tag':tags}  
dataframe = pd.DataFrame(frame)    
dataframe.to_excel('data/test.xlsx') 
