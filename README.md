# Ankinotes

Sync plain text notes into Anki cards. Inspired by Andy Matuschak's system for creating Anki flashcards from his plain text notes. 

Ankinotes.py crawls a directory of ```.md``` files looking for text formatted for conversion into Anki cards, which are then added to the Anki SQLite database as new cards. 
New cards are added to a JSON file (mine is here as an example) which is checked to ensure old cards are not duplicated. Moving notes between files does not alter this.
Currently changes to the 'front' of a card are interpreted as a new card which will be added again to the Anki deck, while changes to the 'back' of a card are not synchronised with Anki. 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. It is strongly recommended that you backup your Anki decks each time before using this programme. 
This software is released free of charge under the MIT license (see LICENSE.txt). 

## Syntax

Currently only the default two-sided prompt is supported. 

### Default two-sided prompts

Q: What conditions may cause erythema nodosum?  
A: Infection (TB, streptococci)  
Sarcoidosis  
IBD  
Behcet's  
Cancer/lymphoma  
Drugs (penicillins, sulphonamides, COCP)  
Pregnancy  

Two sided prompts are single discrete paragraphs with an empty line above and below. The front of the card must begin on a newline with 'Q: ', while the back of the card starts on a newline beginning with 'A: '. 


## Use

The anki collection directory is hardcoded. Open the ```ankinotes.py``` file in a text editor and change the anki_home variable. Then go to the ankinotes directory in the terminal and run the following:

```python3 ankinotes.py /path/to/notes/directory```

