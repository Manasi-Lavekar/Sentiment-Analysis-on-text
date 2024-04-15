import streamlit as st
import nltk
from nltk.stem import PorterStemmer
ps=PorterStemmer()
from nltk.tokenize import sent_tokenize
import re

# Function for backend processing
def analyze_text(text):
  
    # Making a list of all the stop words
    data_sw=[]
    with open("Total_stop_words.txt","r+") as f:
        for line in f:
                for word in line.split():
                    if word.isdigit() or word.isalpha():
                        data_sw.append(word)

                        
    # Making a list of all positive words
    data_pos=[]
    with open("positive-words.txt","r") as f:
        for line in f:
            for word in line.split():
                if word.isdigit() or word.isalpha():
                    data_pos.append(word)
                
    # Making a list of all negative words
    data_neg=[]
    with open("negative-words.txt","r") as f:
        for line in f:
            for word in line.split():
                if word.isdigit() or word.isalpha():
                    data_neg.append(word)

    

    # To find distance between two vowels so that in case of two consecutive vowels only one will be counted as a syllable.
    def find_dist(st,en):
        count=0
        count=en-st
        return count

    # To create a list of indexes at which vowels exist in a word
    def cal_vow(word):
        vowels = ['a', 'e', 'i', 'o', 'u']
        return [i + 1 for i, char in enumerate(word.lower()) if char in vowels]
    
    # To calculate the number of syllables and complex words in the content list
    def syllab(content):
        sum_sy = 0
        count_sy = 0
        
        for word in content:
            vow_list = cal_vow(word)
            if len(word) > 1:
                syllables = 1
                for j in range(len(vow_list) - 1):
                    if vow_list[j+1] - vow_list[j] > 1:
                        syllables += 1
                sum_sy += syllables
                if syllables > 2:
                    count_sy += 1
            else:
                sum_sy += 1
        return sum_sy, count_sy
    
        
    # To calculate the number of pronouns
    def pronoun_count(content):
        pronouns=re.compile(r'\b(I|we|ours|my|mine|he|him|she|they|them|me|(?-i:it)|you|her|(?-i:us))\b',re.I)
        pro_list=pronouns.findall(content)
        no_pronouns=len(pro_list)
        return no_pronouns
    
    text_content1=text.split()
    text_content=re.findall(r'\b\w+\b',text)
    
    
    # cleaned the data by removing punctuation marks
    clean=[data2 for data2 in text_content if data2.isdigit() or data2.isalpha()]
    
    # Removed stop words
    clean1=[data2 for data2 in clean if data2 not in data_sw ]
    
    # Stored positive words in a list
    posi_text_content=[data2 for data2 in clean1 if data2 in data_pos]
    
    # Stored negative words in a list
    neg_text_content=[data2 for data2 in clean1 if data2 in data_neg]
    
    # Calculations - positive score, negative score, polarity score, subjectivity score
    Positive_Score=len(posi_text_content)
    Negative_Score=len(neg_text_content)
    Polarity_Score = round((Positive_Score - Negative_Score)/ ((Positive_Score + Negative_Score) + 0.000001),3)
    Subjectivity_Score = round((Positive_Score + Negative_Score)/ ((len(clean1)) + 0.000001),3)
    
    # Converted the content list into string by joining the words
    text_data=" ".join(text_content1)
    
    # Divided the text into sentences to calculate number of sentences
    num_sent=sent_tokenize(text_data)
    
    # Calculations - avg senetence length,avg words per sentence,word count
    
   
    avg_words_sent=len(clean)//len(num_sent)
    word_count=len(clean)
    
    # Calculated total characters in the text to calculate avg word length
    sum_char=0
    for i in clean:
        sum_char=sum_char+len(i)
    avg_sent_len=sum_char//len(num_sent)
    avg_word_len=sum_char//len(clean)
    
    # Calculations - syllable count, complex word count, percentage of complex words, fog index, syllable per word, pronouns count respectively
    syllab_count,no_comp_words=syllab(clean)
    per_comp_words=round((no_comp_words/len(clean)),3)
    fog_index=round((0.4*(avg_sent_len+per_comp_words)),3)
    # syllab_per_word=syllab_count//len(clean)
    no_pronouns=pronoun_count(text_data)
    return [Positive_Score, Negative_Score, Polarity_Score, Subjectivity_Score, avg_sent_len, per_comp_words, fog_index, avg_words_sent, no_comp_words, word_count, syllab_count, avg_word_len, no_pronouns]

# Streamlit frontend
def main():
    st.title('Text Analysis App')
    st.write('Enter your text paragraph below:')
    text_input = st.text_area('Input text', '')
    output_labels=['Positive Score', 'Negative Score', 'Polarity Score', 'Subjectivity Score', 'Average sentence length(in Characters)', 'Percentage Complex words', 'Fog index', 'Average words per sentence', 'Number of Complex words', 'Total Word count', 'Number of Syllables', 'Average word length', 'Number of Pronouns']
    if st.button('Analyze'):
        if text_input:
            st.write('Analyzing...')
            outputs = analyze_text(text_input)
            if outputs:
                st.write('Here are the outputs:')
                for i, output in enumerate(outputs):
                    st.write(f'{output_labels[i]}: {output}')
            else:
                st.error('Failed to get outputs.')
        else:
            st.error('Please enter some text.')

if __name__ == '__main__':
    main()
