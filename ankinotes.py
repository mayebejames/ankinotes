#!/usr/bin/env python3
# ankinotes.py
# Crawls .md notes looking for discrete question/answer paragraphs to
# add to the default anki deck. Maintains a JSON file of added
# cards to prevent re-adding cards with repeat crawls.
#
# Usage: python3 ankinotes.py </Users/usr/notes/folder>
# Accepted flashcard format: "\n\nQ: <question>\nA: <answer>\n\n"
# For example document see example.md in <<github repo>>


# TODO: 
# 1) Implement CRUD: editing/deleting a card edit/deletes both in JSON
# database and in Anki. Currently editing the 'back' of a card edits this
# in the JSON database but not in Anki, changing the 'front' of the card
# is considered a new card and deleted cards are maintained in Anki and
# in the JSON database
# 2) Find out reason for ?BUG: saveJson works only if called before importAnki

import re
import os
import json

from sys import argv
from anki.storage import Collection



def main(notes_dir):
    main_deck = loadJson("anki_deck.json")
    new_deck = {}
    for file in os.listdir(notes_dir):
        if file.endswith(".md"):
            path = notes_dir + '/' + file
            text = openFile(path)
            file_deck = makeCards(text) # cards extracted from this file
            # Add only file_deck cards not in the main_deck to new_deck
            # for import into Anki. 
            new_deck = addNewCards(main_deck, file_deck, new_deck)
            # Merge file deck into main deck:
            main_deck = mergeDict(main_deck, file_deck)
    saveJson("anki_deck.json", main_deck)
    if new_deck: # dictionary evaluates to false if empty
        print(new_deck)
        importAnki(new_deck)
    # ?BUG: saveJson does only saves if called before importAnki



def findCard(text):
    regex = re.compile(r"^Q:\s(.*?)\nA:\s(.*?)$", re.DOTALL)
    match = regex.search(text)
    if match:
        question = match.group(1)
        answer   = match.group(2)
        return(question, answer)
        

def convertNewlines(text):
    '''Replace plaintext \n newlines with anki-compatible <br>. '''
    return text.replace('\n', '<br>')




def makeCards(text):
    cards = {}
    paragraphs = text.split('\n\n')
    for paragraph in paragraphs:
        card = findCard(paragraph)
        if card:
            question = card[0]
            answer = card[1]
            cards[question] = answer
    return(cards)



def importAnki(cards_dict):
    # Find the Anki directory
    anki_home = "/Users/james/Library/Application Support/Anki2/User 1"
    anki_collection_path = os.path.join(anki_home, "collection.anki2")

    # 1. Load the anki collection
    col = Collection(anki_collection_path, log=True)

    # 2. Select the deck
    model = col.models.byName('Basic')
    deck = col.decks.byName('Default')
    col.decks.select(deck['id'])
    col.decks.current()['mid'] = model['id']

    # 3. Create the cards
    for question, answer in cards_dict.items(): 
        note = col.newNote()
        note.fields[0] = convertNewlines(question)
        note.fields[1] = convertNewlines(answer)
        col.addNote(note)

    # 4. Save changes
    col.save()
    pass
  
    

def loadJson(file_path):
    if not os.path.exists(file_path):
        empty_json = {}
        saveJson(file_path, empty_json)
        return(empty_json)
    else:      
        with open(file_path) as f:
            json_data = json.loads(f.read())
        return(json_data)

            
 
    
def saveJson(file_path, json_data):
    with open(file_path, 'w') as f:
        #json.dump(json_data, f)
        f.write(json.dumps(json_data))



def openFile(file_path):
    """Open file in read mode, return file contents"""    
    md_file = open(file_path, 'r')
    file_contents = md_file.read()
    md_file.close()
    return file_contents
    


def addNewCards(old_dict, comparison_dict, new_dict):
    """Compare old_dict and comparison_dict, add only those keys not in 
       old_dict to the new_dict."""
    if old_dict:
        for k, v in comparison_dict.items():
            if k not in old_dict:
                new_dict[k] = comparison_dict[k]
        return(new_dict)
    else:
        return(comparison_dict)
    



def mergeDict(recipient_dict, donor_dict):
    """Merge donor_dict into recipient_dict:
       Add new k,v pairs to recipient_dict, 
       update v in recipient_dict if different in donor_dict.
       Return recipient_dict. 
    """
    for k, v in donor_dict.items():
        if k in recipient_dict:
            if recipient_dict[k] != donor_dict[k]:
                recipient_dict[k] = donor_dict[k]
        else:
            recipient_dict[k] = donor_dict[k]
    return(recipient_dict)

  


    
        


if __name__ == "__main__":
    """ This is executed when run from the command line 
    1st arg: notes folder path
    """
    main(argv[1])

    
