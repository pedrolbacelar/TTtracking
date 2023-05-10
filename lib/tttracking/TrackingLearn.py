import pyttsx3
from .helper import Helper
from .interfaceDB import interfaceDB
from .components import Card   

class LearnTracker:
    def __init__(self, name, rate=130, voice='it-it'):
        self.helper = Helper()

        #--- Basic settings
        self.name = name
        self.rate = rate
        self.voice = voice
        self.alive = True
        self.next_tracking = "task"

        #--- Init engine
        self.engine = pyttsx3.init()
        #--- Set voice settings
        self.engine.setProperty('voice', self.voice)
        #--- Set the speaking speed rate
        self.engine.setProperty('rate', self.rate)

        #--- Database Management
        self.cards_interfaceDB = interfaceDB("learn")

        #--- Dictionary with all the commands
        self.commands = {
            "add": self.command_add,
            "review": self.command_review,
            "show": self.command_show,
            "switch": self.command_switch,
            "kill": self.command_kill
        }


    # ------- Main Loop -------
    def run(self):
        while self.alive:
            #--- Receive command from user
            command = input(f"{self.name}>>> ")

            #--- Parse command into the correct functions
            self.parse_command(command)

        #--- Switch to the next tracking
        return self.next_tracking
    

    # ------- Commands -------
    # CARDS TYPES:
    # - NEW CARD: card that was never reviewed
    # - LEARNING CARD: card that is being reviewed
    # - FAILED CARD: card that was reviewed but the user failed to remember

    # DATABASE STRUCTURE:
    # - cards_table: [card_id, front, back, type, last_review, next_review, interval, nreviews, nfailed]
    
    # CARD CLASS STRUCTURE:
    # - Card: [card_id, front, back, type, last_review, next_review, interval, nreviews, nfailed]
    # update_correct(): update card after correct answer - interval = interval * 2 (update next_review)
    # update_failed(): update card after failed answer -  interval = 1 (update next_review)


    # COMMANDS:
    # - Init
        # Show number of card to reviewed until today
    # - command add (new card)
       # - add <italian phrase> (front card)
       # - (>> add portuguese version) portuguese phrase (back card)
    # - command review (learning card)
        # - review <card_id> (front card) (reviewed a specific card)
            # >> show front card and speech it
            # wait for commands (input(">>> status"))
            # if "" (enter) : card was answered corrected >> update card
            # if "r": repeat the speech
            # if "f": card was answered incorrectly >> update card (reset card internal counter)"        

    # - command show (show cards) ONLY cards with next review day before today
        # - show new (show new cards)
        # - show learning (show learning cards)
        # - show failed (show failed cards)
        # - show (show all cards) 

    def command_add(self, secondary_command):
        """
        addd <italian phrase> (front card)
        (>> add portuguese version) portuguese phrase (back card)
        """

        #--- Check if the secondary command is not empty
        if len(secondary_command) > 0:

            #--- Get the front card
            front = " ".join(secondary_command)
            #--- Get the back card
            back = input(f"\033[33m Insert Back >>> \033[0m ")

            #--- Create a card object
            new_card = Card(front, back)

            #--- Add the card to the database
            self.cards_interfaceDB.insert_card(new_card)
        
        else:
            self.helper.printer("[ERROR] Command add needs a phrase", color='red')


    def command_review(self, secondary_command):
        """
        review <card_id> (front card) (reviewed a specific card)
        """

        #--- Check if the secondary command is not empty
        if len(secondary_command) > 0:
            #--- Get the card id
            card_id = secondary_command[0]

            #--- Get the card from the database
            card = self.cards_interfaceDB.get_card(card_id)
        
        else:
            print("Revieweing a random card...")
            #--- Get a random card from the database
            card = self.cards_interfaceDB.get_card_open_random()

        #--- Check if the card exists
        if card is not None:
            #--- Check if the card is a learning card
            #--- Show the front card
            self.helper.printer(f"Card Front: {card.front}", color='brown')
            #--- Say the front card
            self.say(card.front)

            repeat = True
            while repeat:

                #--- Wait for the user input
                status = input(">>> ")

                #--- Check the status
                if status == "":
                    #--- Update the card
                    next_review = card.update_review(success= True)
                    self.helper.printer(f"Card Successfully Updated. Next Review at {next_review}", color='green')
                    #--- Update card in the table
                    self.cards_interfaceDB.update_card(card)
                    repeat = False
                
                elif status == "r":
                    print("Saying the card again...")
                    #--- Say the front card
                    self.say(card.front)
                    #--- Update card in the table
                    self.cards_interfaceDB.update_card(card)
                    repeat = True

                elif status == "f":
                    self.helper.printer(f"Card Back: {card.back}", color='brown')
                    #--- Update the card
                    next_review=  card.update_review(success= False)
                    self.helper.printer(f"Card Failed. Next Review at {next_review}", color='red')

                    #--- Update card in the table
                    self.cards_interfaceDB.update_card(card)

                    repeat = False

                else:
                    self.helper.printer("[ERROR] Status not found", color='red')
        else:
            self.helper.printer("[ERROR] Card not found", color='red')
        
    def command_show(self, secondary_command):
        """
        show new (show new cards)
        show learning (show learning cards)
        show failed (show failed cards)
        show (show all cards)
        """

        #--- Check if the secondary command is not empty
        if len(secondary_command) > 0:
            #--- Get the type of cards
            card_type = secondary_command[0]

            #--- Get the cards from the database
            if card_type == "new":
                cards = self.cards_interfaceDB.get_cards_open_new()
            elif card_type == "learning":
                cards = self.cards_interfaceDB.get_cards_open_learning()
            elif card_type == "failed": 
                cards = self.cards_interfaceDB.get_cards_open_failed()
            
        else:
            #--- Get all the cards from the database
            cards = self.cards_interfaceDB.get_cards_opens()

        #--- Check if there are cards
        if len(cards) > 0:
            #--- Print the cards
            self.helper.printer("Showing all open cards:")
            print("   CARD IDs   |   CARD NAME")

            for card in cards:
                card_id = card.get_id()
                if card_id < 10:
                    print(f"       {card_id}      |   \033[35m{card.get_type()}\033[0m - {card.get_front()}")
                elif card_id > 9 and card_id < 100:
                    print(f"      {card_id}      |   \033[35m{card.get_type()}\033[0m - {card.get_front()}")
                elif card_id > 99:
                    print(f"     {card_id}      |   \033[35m{card.get_type()}\033[0m - {card.get_front()}")

        else:
            self.helper.printer("[ERROR] No cards found", color='red')

    def command_switch(self, secondary_command):
        """
        switch task
        switch fin
        switch daily
        """
        
        #--- Take the name of swicthing tracking
        self.next_tracking = secondary_command[0]
        
        #--- Kill the condition of the main loop
        self.alive = False

        self.helper.printer(f"---- Swtiching to Tracking '{self.next_tracking}' ----", 'brown')

    def command_kill(self, secondary_command):
        self.helper.kill(self.name)

    # --------- Helping Functions ------------
    def parse_command(self, command):
        args = command.split()
        if args[0] in self.commands:
            secondary_command = args[1:]
            self.commands[args[0]](secondary_command)
        else:
            self.helper.printer(f"[ERROR] Command {command} not found", color='red')

    # ------- Actions Functions -------
    def say(self, text):
        #--- Run the speech
        self.engine.say(text)
        self.engine.runAndWait()
    def show_voices(self):
        voices = self.engine.getProperty('voices')
        for voice in voices:
            print('---------------------')
            print('ID:', voice.id)
            print('Name:', voice.name)
            print('Languages:', voice.languages)
            print('Gender:', voice.gender)
