"""
Created on Apr 14, 2015

@author: Jay
"""

# shop element test for $unnamedRPG
from math import sin

import pygame

from collections import Counter

pygame.init()


class Player(object):
	def __init__(self, player_gold):
		self.inventory = Counter()
		self.player_gold = player_gold

	def add_to_inventory(self, item_to_add):
		self.inventory[item_to_add] += 1

	def print_inventory(self):
		print self.inventory


class Background(object):
	def __init__(self, color):
		self.color = color
		update_queue.append(self)

	def update_screen(self):
		shop_display.fill(self.color)


class TextObject(object):
	def __init__(self, message, textx, texty, color, is_permanent, time_to_death, is_centered):
		self.message = message
		self.textx = textx
		self.texty = texty
		self.color = color
		self.is_permanent = is_permanent
		self.time_to_death = time_to_death
		self.is_centered = is_centered
		update_queue.append(self)

	def make_text(self):
		on_screen = font.render(self.message, True, self.color)
		if self.is_centered:
			thing = on_screen.get_rect()
			self.textx = (display_x / 2) - (thing.width / 2)
			self.texty = (display_y / 2) - (thing.height / 2)
		shop_display.blit(on_screen, [self.textx, self.texty])

	def is_temp(self):
		if not self.is_permanent and self.time_to_death > 0:
			self.time_to_death -= 1
		if not self.is_permanent and self.time_to_death <= 0:
			update_queue.remove(self)

	def update_screen(self):
		self.is_temp()
		self.make_text()


class Shop(object):
	menuSelect = pygame.mixer.Sound("FF7ok.wav")
	menuCancel = pygame.mixer.Sound("FF7cancel.wav")
	menuWrong = pygame.mixer.Sound("FF7no.wav")
	menuMove = pygame.mixer.Sound("FF7move.wav")
	menuReady = pygame.mixer.Sound("FF7ready.wav")

	def __init__(self, name, greeting, in_shop, merchant_gold):
		self.inventory = Counter({"Potion": 50, "Antidote": 20, "Phoenix Down": 15})
		self.merchant_gold = merchant_gold
		self.greeting = greeting
		self.name = name
		self.in_shop = in_shop
		self.shop_background = Background([0, 0, 0])
		self.shop_greeting = TextObject(self.greeting, 50, 50, (255, 255, 255), True, 0, False)
		self.shop_background.update_screen()
		self.shop_greeting.make_text()
		self.selected = "None"
		self.successful_buy = "none"
		self.item_names = []
		itemy = 75
		for item in self.inventory:
			self.item_list = TextObject(item, 75, itemy, (255, 255, 255), True, 0, False)
			self.item_names.append(item)
			itemy += 25
		self.item_list.make_text()
		self.temp_greet = TextObject("Welcome to my shop!", 0, 0, (255, 255, 255), False, 1000, True)
		self.select_cursor = Cursor("shopcursor.png", 10, 75, 0)
		self.selected_item = 0
		self.menuReady.play()

	def buy_item(self):
		if update_queue[-1] != self.select_cursor:
			update_queue.pop()
		self.selected = self.item_names[self.selected_item]
		if 1 * master_item_list[self.selected] <= player_one.player_gold and 1 <= self.inventory[self.selected]:
			self.actual_text = "Thank you for purchasing {}".format(self.selected)
			self.successful_buy = TextObject(self.actual_text, 0, 0, (255, 255, 255), False, 2000, True)
			player_one.add_to_inventory(self.selected)
			player_one.player_gold -= master_item_list[self.selected]
			self.merchant_gold += master_item_list[self.selected]
			self.inventory[self.selected] -= 1
			self.menuSelect.play()
		elif 1 * master_item_list[self.selected] > player_one.player_gold:
			self.actual_text = "You can't afford any more {}s".format(self.selected)
			self.failed_buy = TextObject(self.actual_text, 0, 0, (255, 255, 255), False, 2000, True)
			self.menuWrong.play()
		elif self.inventory[self.selected] == 0:
			self.actual_text = "Sorry, I don't have any more {}s".format(self.selected)
			self.failed_buy = TextObject(self.actual_text, 0, 0, (255, 255, 255), False, 2000, True)
			self.menuWrong.play()

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.in_shop = False
			if event.type == pygame.KEYDOWN:
				self.menuWrong.stop()
				self.menuSelect.stop()
				self.menuMove.stop()
				key = pygame.key.get_pressed()
				if key[pygame.K_ESCAPE]:
					self.in_shop = False
				if key[pygame.K_RETURN]:
					self.buy_item()
				if key[pygame.K_UP]:
					self.selected_item -= 1
					if self.selected_item < 0:
						self.select_cursor.targetypos = (len(self.inventory) - 1) * 25 + 75
						self.selected_item = len(self.inventory) - 1
					else:
						self.select_cursor.ychange = -25
					self.select_cursor.move_cursor()
					self.menuMove.play()
				if key[pygame.K_DOWN]:
					self.selected_item += 1
					if self.selected_item > len(self.inventory) - 1:
						self.select_cursor.targetypos = 75
						self.selected_item = 0
					else:
						self.select_cursor.ychange = +25
					self.select_cursor.move_cursor()
					self.menuMove.play()

		for item in update_queue:
			item.update_screen()
		pygame.display.update()


class Cursor(object):
	def __init__(self, image, xpos, ypos, ychange):
		self.image = image
		self.xpos = xpos
		self.ypos = ypos
		self.ychange = ychange
		self.targetypos = self.ypos
		self.targetxpos = self.xpos
		self.timer = 0
		update_queue.append(self)

	def update_screen(self):
		self.timer += 0.1
		if (self.targetypos - self.ypos) > 0:
			self.ypos += 0.01 *(self.targetypos - self.ypos)
		else:
			self.ypos -= 0.01 * (abs(self.targetypos - self.ypos))
		self.xpos += 0.05 * sin(self.timer/10)

		display_image = pygame.image.load(self.image)
		shop_display.blit(display_image, [self.xpos, self.ypos])
		self.ychange = 0

	def move_cursor(self):
		self.targetypos += self.ychange

update_queue = []
display_x = 400
display_y = 400
display_size = display_x, display_y
shop_display = pygame.display.set_mode(display_size)
font = pygame.font.SysFont(None, 25)
item_shop = Shop("Jay's Shop", "What would you like to buy?", True, 1500)
player_one = Player(30000)
master_item_list = Counter({"Potion": 50, "Antidote": 25, "Phoenix Down": 150})


while item_shop.in_shop:
	item_shop.handle_events()

pygame.quit()
quit()
'''


potionPrice = 50
userGold = 100
merchantGold = 0
merchantPotionStock = 1

def buyitem(quantity, cost, stock):
	howmany = quantity
	howmuch = cost
	onhand = stock
	if howmany <= onhand and howmuch <= userGold:
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
				successfulPurchase = buyitem(1, potionPrice, merchantPotionStock)
				if successfulPurchase:
					menuSelect.play()
					userGold -= 50
					merchantGold = + 50
					merchantPotionStock -= 1
				if not successfulPurchase:
					menuWrong.play()
	shopDisplay.fill((255, 255, 255))
	displaytext("What would you like to buy?", 50, 50, (0, 0, 0))
	displaytext("a. Potion - %i gold" % (int(50)), 75, 75, (0, 0, 0))
	pygame.display.update()
'''


