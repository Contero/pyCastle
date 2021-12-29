import msvcrt
import os
import colorama
from colorama import Cursor
colorama.init()

class room:
    def __init__(self):
        self.layout=[]
        self.description=""
        self.adjacent=""
    def draw(self):
        os.system('cls')
        for row in self.layout:
            print(row);
        print(self.description)

class Coords:
    row=0
    column=0
    def __init__(self,row,column):
        self.row=row
        self.column=column

class GameState:
    currentRoom=0
    def roomIndex():
        return GameState.currentRoom - 1
    
class Hero:
    coords=Coords(17,13)
    newCoords=Coords(0,0)
    face="\u2663"
    def draw(self):
        print(Cursor.POS(self.coords.column,self.coords.row)+self.face)
    def clear(self):
        print(Cursor.POS(self.coords.column,self.coords.row)+' ')
    def getRoom(self, direction, adjacent):
        index=adjacent.find(direction)
        try:
             GameState.currentRoom = int(adjacent[index + 1: index+3])
        except:
            GameState.currentRoom = int(adjacent[index + 1: index+2])
    def move(self, direction, room):
        if direction == "N":
            self.newCoords=Coords(self.coords.row-1,self.coords.column)
        elif direction == "E":
            self.newCoords=Coords(self.coords.row,self.coords.column+1)
        elif direction == "S":
            self.newCoords=Coords(self.coords.row+1,self.coords.column)
        elif direction == "W":
            self.newCoords=Coords(self.coords.row,self.coords.column-1)
        
        #Collision Checks
        #left the room?
        if self.newCoords.row < 1 or self.newCoords.row > 18 or self.newCoords.column < 1 or self.newCoords.column > 24:
            #moveRooms
            self.getRoom(direction, room.adjacent)
            if direction == "N":
                self.coords.row=18
            elif direction == "S":
                self.coords.row=1
            elif direction == "E":
                self.coords.column=1
            elif direction == "W":
                self.coords.column=24
            return True
        #same room look for objects
        destination=room.layout[self.newCoords.row-1][self.newCoords.column-1]
        if destination == " ":
            #Good to move
            self.clear()
            self.coords=self.newCoords
            self.draw()
        elif destination == "U" or destination == "D":
            #stairs
            self.getRoom(destination, room.adjacent)
            return True
        return False
            

def loadRooms(rooms):
    file=open("castle.ran",'r',encoding="cp437")
    for i in range(83):
        rooms.append(room())
        temp=""
        for l in range(18):
            temp=file.read(24)
            rooms[i].layout.append(temp)
        temp = ""
        for l in range(5):
            temp=temp + file.read(25) + "\n"
        rooms[i].description=temp
        rooms[i].adjacent = file.read(18)
    file.close()

def main():
    rooms=[]
    GameState.currentRoom=1
    playing=True
    try:
        loadRooms(rooms)
    except:
        print("Error loading data file")
        quit()
    hero=Hero()
    rooms[GameState.roomIndex()].draw()
    hero.draw()
    while playing:
        key=ord(msvcrt.getch())
        if key==27:
            quit()
        else:
            if key==224:
                key=ord(msvcrt.getch())
                if key==72:
                    newRoom=hero.move("N", rooms[GameState.roomIndex()])
                elif key==77:
                    newRoom=hero.move("E", rooms[GameState.roomIndex()])
                elif key==80:
                    newRoom=hero.move("S", rooms[GameState.roomIndex()])
                elif key==75:
                    newRoom=hero.move("W", rooms[GameState.roomIndex()])
            if newRoom:
                rooms[GameState.roomIndex()].draw()
                hero.draw()

    
main()
