#Antakshiri: Human vs Bot
import random
import abc

#An abstract class is a class that represents (heads) a category of classes.
#Example: Shape, Vehicle, Animal, Player
#It cannot be instantiated.
#It is inherited and used.
#It has zero to many abstract methods.
#In Python, an abstract class inherits abc.ABC

class Player(abc.ABC):
    def __init__(self, lyrics):
        self._lyrics_ = lyrics
        self._lyrics_.sort()
        self._score_ = 0

    def increment_score(self):
        self._score_ += 1

    def get_score(self):
        return self._score_

    def has_more_songs(self):
        return  len(self._lyrics_) != 0

    #An abstract method represents an operation that cannot be defined at current level;
    #rather it can be defined at the derived class level only.
    #Example: area() of Shape, move() of Animal, conduct() of Exam, ...

    #An abstract method is a method with signature only and no body.
    #It's dispatch table entry is None.
    #It makes the class an abstract class.
    #It must be overridden by the derived class.
    #In Python, an abstract method is decorated as abc.abstractmethod
    @abc.abstractmethod
    def play(self, start_char):
        pass


class Bot(Player):
    def __init__(self, lyrics):
        Player.__init__(self, lyrics)
        self.opponent_losses = []

    def add_to_opponents_loss(self, loss_char):
        self.opponent_losses.append(loss_char)

    def __search_lyrics__(self, start_char):
        options = []
        if start_char == '':
            for i, l in enumerate(self._lyrics_):
                options.append((i, l))
        else:
            for i, l in enumerate(self._lyrics_):
                if l[0].lower() == start_char.lower():
                    options.append((i,l))

        return options

    def __get_opponents_losing_option__(self, options):
        for i, l in options:
            if l[-1] in self.opponent_losses:
                return (i,l)

        return options[0]

    def play(self, start_char):
        did_pass = False
        options = self.__search_lyrics__(start_char)
        if len(options) == 0:
            did_pass = True
            print('Bot passes, can sing any song')
            start_char = ''
            options = self.__search_lyrics__(start_char)

        current_song = self.__get_opponents_losing_option__(options)
        bot_song = self._lyrics_.pop(current_song[0])
        print('Bot sings {}'.format(bot_song))
        next_song = bot_song[-1]

        return did_pass, next_song

class Human(Player):
    def __init__(self, lyrics, name):
        Player.__init__(self, lyrics)
        self.__name__ = name

    def get_name(self):
        return self.__name__.title()

    def play(self, start_char):
        did_pass = False

        while True:
            if start_char == '':
                print('{} please sing any song'.format(self.get_name()))
            else:
                print('{} please sing a song beginning with {}'.format(self.get_name(), start_char))

            for i,l in enumerate(self._lyrics_, start= 1):
                print('{:3d}) {}'.format(i, l))

            print('{:3d}) {}'.format(-1, 'To pass'))
            ch = int(input())

            if ch == -1 and not did_pass:
                did_pass = True
                start_char = ''
                print('{} passes, Bot gets a point '. format(self.get_name()))
            elif ch < -1 or ch > len(self._lyrics_) or (did_pass and start_char!= '') or (start_char != '' and self._lyrics_[ch-1][0].lower() != start_char.lower()):
                print('Wrong Choice, play again')
            else:
                #choice made
                current_song = self._lyrics_.pop(ch-1)
                print('{} sings {}'.format(self.get_name(), current_song))
                next_song = current_song[-1]
                break

        return did_pass, next_song

class Antakshiri:
    def __init__(self, data_source):
        lyrics = self.__get_lyrics__(data_source)
        human = Human(lyrics.pop(), 'Anil')
        bot = Bot(lyrics.pop())
        self.__players__ = [human, bot]


    #An operation for internal use
    def __load_lyrics__(self, data_source):
        all_lyrics = []
        #open the data source (file) for reading
        f_handle = open(data_source, 'r')

        #read the file data and load in a list
        for a_lyric in f_handle:
            a_lyric = a_lyric.strip()#clean the preceeding and trailing spaces, '\n', ...
            all_lyrics.append(a_lyric)

        #close the file
        f_handle.close()

        return all_lyrics

    def __get_lyrics__(self,data_source):
        #fetch
        temp = self.__load_lyrics__(data_source)
        #distribute
        random.shuffle(temp)
        lyrics = []
        lyrics.append(temp[0::2])
        lyrics.append(temp[1::2])
        random.shuffle(lyrics)
        return lyrics

    def __toss__(self):
        print('Bot flips the coin and {} makes a call (heads/tails)'.format(self.__players__[0].get_name()))
        call = input().lower()
        coin_status = random.choice(['heads', 'tails'])
        return  call == coin_status

    def play_antakshiri(self):
        game_on= True

        current_player =  0 if self.__toss__() else 1

        start_char = ''
        while game_on:
            copy_start_char = start_char
            did_pass, start_char = self.__players__[current_player].play(start_char)
            current_player = (current_player + 1)% 2
            if did_pass:
                if current_player == 1:
                    self.__players__[1].add_to_opponents_loss(copy_start_char)
                self.__players__[current_player].increment_score()

            game_on = self.__players__[0].has_more_songs() and self.__players__[1].has_more_songs()

        score_player = self.__players__[0].get_score()
        score_bot = self.__players__[1].get_score()
        print('{} score : {}'.format(self.__players__[0].get_name(), score_player))
        print('Bots score : {}'.format( score_player))

        if score_player == score_bot :
            print('Antakshiri (Summer 22) : Game Tied')
        elif score_player > score_bot :
            print('{} wins Antakshiri (Summer 22)'.format(self.__players__[0].get_name()))
        else:
            print('Bot wins Antakshiri (Summer 22)')

def main():
    game = Antakshiri('lyrics.txt')
    game.play_antakshiri()

main()