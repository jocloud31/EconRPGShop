'''
Created on Apr 14, 2015

@author: Jay
'''

#shop element test for $unnamedRPG
import pygame
import random

pygame.init()

menuSelect = pygame.mixer.Sound("FF7ok.wav")
menuCancel = pygame.mixer.Sound("FF7cancel.wav")
menuWrong = pygame.mixer.Sound("FF7no.wav")
menuMove = pygame.mixer.Sound("FF7move.wav")

shopDisplay = pygame.display.set_mode((400,400))
pygame.display.set_caption("Welcome to Jay's shop!")
font = pygame.font.SysFont(None, 25)

potionPrice = 50
userGold = 100
merchantGold = 0
merchantPotionStock = 1

inShop = True

def displayText(msg,textX,textY,color):
    on_screen = font.render(msg, True, color)
    shopDisplay.blit(on_screen, [textX,textY])

def buyItem(name,quantity,cost,stock):
    itemName = name
    howMany = quantity
    howMuch = cost
    onHand = stock
    if howMany <= onHand and howMuch <= userGold:
        return True
    else:
        return False
        
while inShop:
    for event in pygame.event.get():
        print(userGold)
        print(merchantPotionStock)
        if event.type == pygame.QUIT:
            inShop = False
        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                inShop = False
            if key[pygame.K_a]:
                successfulPurchase = buyItem("Potion",1,potionPrice,merchantPotionStock)
                if successfulPurchase:
                    menuSelect.play()
                    userGold -= 50
                    merchantGold =+ 50
                    merchantPotionStock -= 1
                if not successfulPurchase:
                    menuWrong.play()
    shopDisplay.fill((255,255,255))
    displayText("What would you like to buy?",50,50,(0,0,0))
    displayText("a. Potion - %i gold" % (int(50)),75,75,(0,0,0))
    pygame.display.update()            
            
            
pygame.quit()
quit()

