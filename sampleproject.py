from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image,ImageTk
import language_tool_python
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import string
import io

counter=1
file=open("questions.txt","r")
q=[line.rstrip('\n') for line in file]
totmark=[0,0,0,0,0]

def nex():
    global counter
    if(counter<5):
        counter=counter+1
        ques.set(str(q[counter-1]))
        entry.delete("1.0", "end")
   
    else:
        messagebox.showwarning("Limit Exceeded","Sorry, No more questions available!")
    #print(counter)

def prev():
    global counter
    if(counter>1):
        counter=counter-1
        ques.set(str(q[counter-1]))
    else:
        messagebox.showwarning("Limit Exceeded","This is the first question!")
    #print(counter)


def enFunc():
    global counter
    
    ans = entry.get('1.0','end')
    ab = str(ans)
    print(ab)
    print(type(ab))
    n=0
    for line in ans:
        words=[line.split(' ') for line in ans]
    # n=len(words)
    n = len(ans.split())
    print(n)
    if(n>=100):
        marks1=10
    elif(n>=90 and n<100):
        marks1 = 9
    elif(n>=80 and n<90):
        marks1 = 8
    elif(n>=60 and n<80):
        marks1 = 6
    elif(n>=40 and n<60):
        marks1 =5
    elif(n>=20 and n<40):
        marks1 = 4
    elif(n>=10 and n<20):
        marks1 = 2
    elif(n==1 or n==0):
        marks1 = 0
    else:
        marks1=1

    a=marks1

    tool = language_tool_python.LanguageTool('en-US')
    count=0
    text=str(ans)
    txtlen=len(text.split())
    setxt = set(text.split())
    setlen = len(setxt)
    matches=tool.check(text)
    #print("Error:",matches)
    print("No. of Errors=",len(matches))
    noOfError=len(matches)
    if(n==0 or n==1):
        marks2 = 0
    elif (noOfError<=2 and n>1):
        marks2 = 10
    elif (noOfError<=4 and noOfError>2):
        marks2 = 9  
    elif (noOfError<=6 and noOfError>4):
        marks2 = 8
    elif (noOfError<=10 and noOfError>6):
        marks2 = 5
    elif (noOfError<=12 and noOfError>10):
        marks2 = 3
    elif (noOfError<=15 and noOfError>12):
        marks2 = 2
    else:
        marks2 = 1

    b = marks2

    with open('answer'+str(counter)+'.txt','r') as file1:
        abb = file1.read().replace('\n', '')
    print(abb)
    print(type(abb))
    
    file1.close()

    faculty_keywords = faculty_answer(abb)
    student_keywords = student_Answer(ab)
    print("Faculty Keywords \n")
    print(faculty_keywords)
    print("Student Keywords \n")   
    print(student_keywords)

    print(set(faculty_keywords)&set(student_keywords))
    mat_key = len(set(faculty_keywords)&set(student_keywords))
    print(mat_key)
    per_key = ((mat_key/len(faculty_keywords))*100)
    print(per_key)
    if(n==0 or n==1):
        marks3 = 0
    elif (per_key>90):
        marks3 = 30
    elif (per_key>80 and per_key<=90):
        marks3 = 27  
    elif (per_key>70 and noOfError<=80):
        marks3 = 24
    elif (per_key>60 and noOfError<=70):
        marks3 = 21
    elif (per_key>50 and noOfError<=60):
        marks3 = 18
    elif (per_key>40 and noOfError<=50):
        marks3 = 15
    elif (per_key>20 and noOfError<=40):
        marks3 = 9
    elif (per_key>1 and noOfError<=20):
        marks3 = 3      
    else:
        marks3 = 0
   
    c = marks3

    d = a + b + c

    print("Marks obtained for length = ",+a,"/10") 
    print("Marks obtained after parsing=",marks2,"/10")
    print("Marks for keywords matching =",marks3,"/30")
    print("Marks obtained out of 50 is=",d,"/50")


    ss = (d/50)*2
    tot = round(ss, 1)
    m="\nAnswer is submitted"
    messagebox.showinfo("Result",m)
    
    global totmark
    totmark[counter-1]=tot

    file2= open("user.txt",'a')
    file2.write("\nQuestion " +str(counter)+"\n")
    file2.write("Marks obtained for length = "+str(a)+"/10 \n")
    if len(matches) == 0:
        file2.write("Number of Grammatical error = "+str(0)+"\n")
    else:
        file2.write("Number of Grammatical error = "+str(matches)+"\n")
    file2.write("Marks obtained after parsing = "+str(b)+"/10 \n")

    file2.write("\n#####Faculty Answer Keywords : \n")
    file2.writelines("%s\n" % place for place in faculty_keywords)

    file2.write("\nNumber of Keywords Match = "+str(mat_key)+"/15 \n")
    file2.write("Marks obtained for keyword match = "+str(c)+"/30 \n")
    file2.write("Marks obtained for this Question = "+str(tot)+"/2 \n")

    file2.close()

def faculty_answer(abb):
    
    abb = abb.lower()

    text = word_tokenize(abb)
    print(text)
    POS_tag = nltk.pos_tag(text)


    wordnet_lemmatizer = WordNetLemmatizer()
    adjective_tags = ['JJ','JJR','JJS']
    lemmatized_text = []
    for word in POS_tag:
        if word[1] in adjective_tags:
            lemmatized_text.append(str(wordnet_lemmatizer.lemmatize(word[0],pos="a")))
        else:
            lemmatized_text.append(str(wordnet_lemmatizer.lemmatize(word[0]))) #default POS = noun

    POS_tag = nltk.pos_tag(lemmatized_text)

    stopwords = []
    wanted_POS = ['NN','NNS','NNP','NNPS','JJ','JJR','JJS','VBG','VBP','FW','RB'] 
    for word in POS_tag:
        if word[1] not in wanted_POS:
            stopwords.append(word[0])
    punctuations = list(str(string.punctuation))
    stopwords = stopwords + punctuations
    stopword_file = open("long_stopwords.txt", "r")
    lots_of_stopwords = []

    for line in stopword_file.readlines():
        lots_of_stopwords.append(str(line.strip()))

    stopwords_plus = []
    stopwords_plus = stopwords + lots_of_stopwords
    stopwords_plus = set(stopwords_plus)

    processed_text = []
    for word in lemmatized_text:
        if word not in stopwords_plus:
            processed_text.append(word)

    vocabulary = list(set(processed_text))

    import numpy as np
    import math
    vocab_len = len(vocabulary)
    weighted_edge = np.zeros((vocab_len,vocab_len),dtype=np.float32)
    score = np.zeros((vocab_len),dtype=np.float32)
    window_size = 3
    covered_coocurrences = []

    for i in range(0,vocab_len):
        score[i]=1
        for j in range(0,vocab_len):
            if j==i:
                weighted_edge[i][j]=0
            else:
                for window_start in range(0,(len(processed_text)-window_size+1)):
                        
                    window_end = window_start+window_size
                        
                    window = processed_text[window_start:window_end]
                        
                    if (vocabulary[i] in window) and (vocabulary[j] in window):
                            
                        index_of_i = window_start + window.index(vocabulary[i])
                        index_of_j = window_start + window.index(vocabulary[j])
                            
                            # index_of_x is the absolute position of the xth term in the window 
                            # (counting from 0) 
                            # in the processed_text
                            
                        if [index_of_i,index_of_j] not in covered_coocurrences:
                            weighted_edge[i][j]+=1/math.fabs(index_of_i-index_of_j)
                            covered_coocurrences.append([index_of_i,index_of_j])

    inout = np.zeros((vocab_len),dtype=np.float32)

    for i in range(0,vocab_len):
        for j in range(0,vocab_len):
            inout[i]+=weighted_edge[i][j]

    MAX_ITERATIONS = 50
    d = 0.9
    threshold = 0.0001 #convergence threshold

    for iter in range(0,MAX_ITERATIONS):
        prev_score = np.copy(score)
            
        for i in range(0,vocab_len):
                
            summation = 0
            for j in range(0,vocab_len):
                if weighted_edge[i][j] != 0:
                    summation += (weighted_edge[i][j]/inout[j])*score[j]
                        
            score[i] = (1-d) + d*(summation)
            
        if np.sum(np.fabs(prev_score-score)) <= threshold: #convergence condition
            print ("Converging at iteration "+str(iter)+"....")
            break

    for i in range(0,vocab_len):
        print ("Score of "+vocabulary[i]+": "+str(score[i]))

    phrases = []
    phrase = " "
    for word in lemmatized_text:
            
        if word in stopwords_plus:
            if phrase!= " ":
                phrases.append(str(phrase).strip().split())
            phrase = " "
        elif word not in stopwords_plus:
            phrase+=str(word)
            phrase+=" "
    print("\n")
    print("Partitioned Phrases (Candidate Keyphrases): \n")
    print (phrases)

    unique_phrases = []

    for phrase in phrases:
        if phrase not in unique_phrases:
            unique_phrases.append(phrase)
    print("\n")
    print ("Unique Phrases (Candidate Keyphrases): \n")
    print (unique_phrases)

    for word in vocabulary:
        #print word
        for phrase in unique_phrases:
            if (word in phrase) and ([word] in unique_phrases) and (len(phrase)>1):
                    #if len(phrase)>1 then the current phrase is multi-worded.
                    #if the word in vocabulary is present in unique_phrases as a single-word-phrase
                    # and at the same time present as a word within a multi-worded phrase,
                    # then I will remove the single-word-phrase from the list.
                unique_phrases.remove([word])
    print("\n")           
    print("Thinned Unique Phrases (Candidate Keyphrases): \n")
    print(unique_phrases)  

    phrase_scores = []
    keywords = []
    for phrase in unique_phrases:
        phrase_score=0
        keyword = ''    
        for word in phrase:
            keyword += str(word)
            keyword += " "
            phrase_score+=score[vocabulary.index(word)]
        phrase_scores.append(phrase_score)
        keywords.append(keyword.strip())

    i=0
    for keyword in keywords:
        print("Keyword: '"+str(keyword)+"', Score: "+str(phrase_scores[i]))
        i+=1

    sorted_index = np.flip(np.argsort(phrase_scores),0)
    print(sorted_index)

    if counter == 3:
        keywords_num = 13
    elif counter == 4:
        keywords_num = 10
    else:
        keywords_num = 15

    # print("\n Keywords:\n")

    for i in range(0,keywords_num):
        print (str(keywords[sorted_index[i]])+", ",)

    am =[]
    for i in range(0,keywords_num):
        am.append(str(keywords[sorted_index[i]]))
    return am

def student_Answer(ab):
    '''Make text lowercase, remove text in sqaure brackets, remove punctuations and remove words with digits'''
    Text = ab.lower()

    text = word_tokenize(Text)
    POS_tag = nltk.pos_tag(text)

    wordnet_lemmatizer = WordNetLemmatizer()
    adjective_tags = ['JJ','JJR','JJS']
    lemmatized_text = []
    for word in POS_tag:
        if word[1] in adjective_tags:
            lemmatized_text.append(str(wordnet_lemmatizer.lemmatize(word[0],pos="a")))
        else:
            lemmatized_text.append(str(wordnet_lemmatizer.lemmatize(word[0]))) #default POS = noun
                


    POS_tag = nltk.pos_tag(lemmatized_text)


    stopwords = []
    wanted_POS = ['NN','NNS','NNP','NNPS','JJ','JJR','JJS','VBG','VBD','VBN','FW','RB'] 

    for word in POS_tag:
        if word[1] not in wanted_POS:
            stopwords.append(word[0])

    punctuations = list(str(string.punctuation))
    stopwords = stopwords + punctuations
    stopword_file = open("long_stopwords.txt", "r")

    lots_of_stopwords = []

    for line in stopword_file.readlines():
        lots_of_stopwords.append(str(line.strip()))

    stopwords_plus = []
    stopwords_plus = stopwords + lots_of_stopwords
    stopwords_plus = set(stopwords_plus)


    processed_text = []
    for word in lemmatized_text:
        if word not in stopwords_plus:
            processed_text.append(word)



    vocabulary = list(set(processed_text))
    # print(vocabulary)

    phrases = []
    phrase = " "
    for word in lemmatized_text:
            
        if word in stopwords_plus:
            if phrase!= " ":
                phrases.append(str(phrase).strip().split())
            phrase = " "
        elif word not in stopwords_plus:
            phrase+=str(word)
            phrase+=" "
    # print("\n")
    # print("Partitioned Phrases (Candidate Keyphrases): \n")
    # print (phrases)

    unique_phrases = []

    for phrase in phrases:
        if phrase not in unique_phrases:
            unique_phrases.append(phrase)
    # print("\n")
    # print ("Unique Phrases (Candidate Keyphrases): \n")
    # print (unique_phrases)

    for word in vocabulary:
        #print word
        for phrase in unique_phrases:
            if (word in phrase) and ([word] in unique_phrases) and (len(phrase)>1):
                    #if len(phrase)>1 then the current phrase is multi-worded.
                    #if the word in vocabulary is present in unique_phrases as a single-word-phrase
                    # and at the same time present as a word within a multi-worded phrase,
                    # then I will remove the single-word-phrase from the list.
                unique_phrases.remove([word])
    # print("\n")           
    # print("Thinned Unique Phrases (Candidate Keyphrases): \n")
    # print(unique_phrases)  

    keywords = []
    for phrase in unique_phrases:
        keyword = ''
        for word in phrase:
            keyword += str(word)
            keyword += " "
        keywords.append(keyword.strip())
    return(keywords)

def finish():
    
    s=0
    for i in totmark:
        s=s+i
    messagebox.showinfo("Total Score","The total score obtained in the test="+str(float(s))+"/10")

def logout():
    root.destroy()




root = Tk()
root.title("Text Window")
root.geometry("1920x1080+0+0")


text_frame = Frame(root,bg="white")
text_frame.place(x=0,y=0,width=1920,height=1080)




label= Label(text_frame,text="ANSWER ALL THE FOLLOWING QUESTIONS",bg="lightyellow",bd=20,font=("times new roman",15,"bold"))
label.place(x=580,y=10)

ques= StringVar()
ques.set(str(q[counter-1]))
labelQ=Label(text_frame,textvariable=ques,text=str(q[0]),width=70, bg="lightyellow", bd=20,font=("times new roman",15,"bold"))
labelQ.place(x=350,y=100)

entry= Text(text_frame,width=110,height=25)
entry.place(x=350,y=200)

prevBtn= Button(text_frame, text = '<', command = prev,font=("times new roman",13 ,"bold"))
prevBtn.place(x=480,y=630)

button1= Button(text_frame, text = 'Submit',command = enFunc,font=("times new roman",13,"bold"))
button1.place(x=750,y=630)

nextBtn= Button(text_frame, text = '>', command = nex,font=("times new roman",13,"bold"))
nextBtn.place(x=1050,y=630)

finishbtn=Button(text_frame,text='Finish',command=finish,font=("times new roman",13,"bold"))
finishbtn.place(x=755,y=680)

logout=Button(text_frame,text='Logout',command=logout,font=("times new roman",13,"bold"))
logout.place(x=1450,y=10)

root.mainloop()

