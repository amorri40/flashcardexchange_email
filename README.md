flashcardexchange_email
=======================

Email script to email you daily flash card questions.

In order to use you need to create a "flashcard_settings.py" in the same directory as main.py, with the following contents:
    
    #personal settings for flashcard emailing script
    sets_to_ask = [2538923,2539316] #the id's of the sets to ask
    number_to_ask_per_set=2
    email="yourgmailemail@gmail.com"
    gmail_password="yourpassword"

    client_id="3bf3b465c728503083ac63d540f6d104" #flashcard exchange client id
