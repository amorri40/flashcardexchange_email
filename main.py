#!/usr/bin/python

import smtplib,requests, flashcard_settings
from email.MIMEText import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint
message_body = ''

def format_question_answer (title_without_spaces, card_no, text, question_or_answer, opposite, image):
    html=''
    html+="<div><a name='"+title_without_spaces+"_"+question_or_answer+"_"+str(card_no)+"'></a>"
    if image != None:
        html+="<img src='"+image+"'></img></br>"
    html+="<p><b>"+str(card_no)+")</b> "+text+"</p>"
    html+=" <a href='#"+title_without_spaces+"_"+opposite+"_"+str(card_no)+"'>("+opposite+")</a></div></br>"
    return html


for set_id in flashcard_settings.sets_to_ask: 

    #get the set data
    r = requests.get('https://api.flashcardexchange.com/v2/sets/'+str(set_id)+'?client_id='+flashcard_settings.client_id+'')#, auth=('user', 'pass'))
    set_json=r.json()[0]
    title = set_json['title']
    title_without_spaces=title.replace(" ","_") #used for the links to the answers/questions
    description = set_json['description']
    has_image = set_json['has_image']

    print set_json
    message_body+="<div style='border: 2px solid; border-radius: 2px; padding: 10px;'><h1>"+title+"</h1>"+description+"</br></br><h2>Questions</h2>"

    all_cards=set_json['cards']
    no_of_cards = len(all_cards)
    answers_html = "<h2>Answers</h2>"

    card_split_minimum=0 #used to split the deck into the number of questions wanted, then get a random value from that half of the deck
    card_split_maximum=0

    number_of_questions_to_ask=flashcard_settings.number_to_ask_per_set
    for current_question_number in range (0,number_of_questions_to_ask):
        card_split_minimum=card_split_maximum
        card_split_maximum=(current_question_number+1)*(no_of_cards/number_of_questions_to_ask)-1
        card_no = randint(card_split_minimum,card_split_maximum)
        this_card = all_cards[card_no]
        question = this_card['front']
        answer = this_card['back']
        question_image=this_card['image_front']
        answer_image=this_card['image_url']
        message_body+=format_question_answer(title_without_spaces, current_question_number, question, "Question", "Answer",question_image)
        answers_html+=format_question_answer(title_without_spaces, current_question_number, answer, "Answer", "Question",answer_image)

    message_body+=answers_html
    message_body+="</div></br>"

#Send the Message
msg = MIMEMultipart('alternative')
msg['Subject'] = 'Daily Flashcards'
msg['From'] = flashcard_settings.email
msg['Reply-to'] = flashcard_settings.email
msg['To'] = flashcard_settings.email
part1 = MIMEText('your email is so plain', 'plain')
part2 = MIMEText(message_body, 'html')
#msg.attach(part1)
msg.attach(part2)

server = smtplib.SMTP('smtp.gmail.com',587) #port 465 or 587
server.ehlo()
server.starttls()
server.ehlo()
server.login(flashcard_settings.email, flashcard_settings.gmail_password)
server.sendmail(flashcard_settings.email, flashcard_settings.email, msg.as_string())
server.close()


