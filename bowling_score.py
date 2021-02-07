import sys
import re

class Bowling():
    def __init__(self):
        self._player = []

    def askForInput(self,question,player='',frame=0,shot=0):
        x = 1
        response = ''
        questions = [
            "How many players (maximum 4):\n",
            "\nEnter player " + str(frame+1) + ":\n",
            "\nHow many pins did " + str(player) + " knock down on shot " + str(shot+1) + " of Frame " + str(frame+1) + ":\n"
        ]
        
        while x:
            response = input(questions[question])
            if response == 'q':
                print('\nGoodbye!')
                x = 0
                sys.exit()

            if len(response) == 0:
                print("\nInvalid number entered, please try again\n")
                continue

            if question == 1:
                x = 0
                return response

            if question == 0:
                if not re.search("^[\d]+$",response):
                    print("\nInvalid number entered, please try again\n")
                elif int(response) < 1:
                    print("\nInvalid number entered, please try again\n")
                elif int(response) > 4:
                    print("\nSorry that's too many players\n")
                else:
                    x = 0
                    return response
            elif question == 2:
                if not re.search("^[\d]+$",response):
                    print("\nInvalid number entered, please try again\n")
                elif int(response) < 0 or int(response) > 10:
                    print("\nInvalid number entered, please try again\n")
                else:
                    x = 0
                    return response


    def createPlayers(self):
        #get player count
        x = 1
        playerCount = int(self.askForInput(0))
        
        #generate player
        for x in range(playerCount):
            name = self.askForInput(1,'',x)
            self._player.append({"name":name,"scores":[],"finalScore":0})
        
        #load Frames
        self.loadFrames()

    def loadFrames(self):
        #loop through players and preload shots array
        for x in self._player:
            for i in range(10):
                x['scores'].append({"frameScore":0,"shots":[0,0]})

    def scoreEntry(self):
        #gather scores for each shot in each frame of each player
        #loop for players
        for x in range(len(self._player)):
            print("\n\nScore Entry For",self._player[x]['name'])
            finalScore = 0
            #loop for frames
            for i in range(len(self._player[x]['scores'])):
                #set shots length
                shots = 2
                cnt = 0
                #loop for shots
                while cnt < shots:
                    pinCnt = int(self.askForInput(2,self._player[x]['name'],i,cnt))
                    #check if first two scores are with in the 10 pin range
                    if cnt == 1 and self._player[x]['scores'][i]['shots'][0] < 10 and pinCnt + self._player[x]['scores'][i]['shots'][0] > 10:
                        print("\nScore is greater than 10 total pins")
                        pinCnt = int(self.askForInput(2,self._player[x]['name'],i,cnt))
                    #set shot value
                    self._player[x]['scores'][i]['shots'][cnt] = pinCnt
                    finalScore+= pinCnt
                    #sum score and determine if third shot is awarded
                    shots += self.scoreCalc(x,i,cnt)
                    cnt+=1
                #add the third shot and set to zero
                if len(self._player[x]['scores'][i]['shots']) < 3:
                    self._player[x]['scores'][i]['shots'].append(0)
            self._player[x]['finalScore'] = finalScore


    def scoreCalc(self,player,frame,shot):
        #check if shot 1 or 2 and if sum equals ten
        #set return to 0
        extraShot = 0
        if sum(self._player[player]['scores'][frame]['shots']) >= 10 and len(self._player[player]['scores'][frame]['shots']) < 3:
            self._player[player]['scores'][frame]['shots'].append(0)
            extraShot = 1
        
        self._player[player]['scores'][frame]['frameScore'] = sum(self._player[player]['scores'][frame]['shots'])
        return extraShot

    def displayScores(self):
        for x in self._player:
            print("\n")
            print(x['name'],"Final Score:",x['finalScore'],"\n")
            head = ""
            top = ""
            mid1 = ""
            mid2 = ""
            mid3 = ""
            btm = ""
            for n in range(len(x['scores'])):
                components = self.drawBox(x['scores'][n],n+1)
                head+= components[0]
                top+= components[1]
                mid1+= components[2]
                mid2+= components[3]
                mid3+= components[4]
                btm+= components[1]
            print(head)
            print(top.strip())
            print(mid1.strip())
            print(mid2.strip())
            print(mid3.strip())
            print(btm.strip())

    def drawBox(self,data,frame):
        #create score box
        top =     " Frame " + str(frame).zfill(2) + "         "
        middle1 = "|################|"
        middle3 = "|       ---------|"
        middle4 = "|Score:" + str(data['frameScore']).zfill(2) + "        |"
        middle2 = "|       |"
        for x in data['shots']:
            middle2+= str(x).zfill(2) + "|"
        return [top,middle1,middle2,middle3,middle4]




if __name__ == "__main__":
    #initiate bowling instance
    game = Bowling()
    #create players
    print("Enter q to exit\n")
    game.createPlayers()
    #gather scores
    game.scoreEntry()
    #print out frames
    game.displayScores()
