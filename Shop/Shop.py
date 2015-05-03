"""
Created on Apr 14, 2015

@author: Jay
"""

# shop element test for $unnamedRPG
import pygame
from math import sin
pygame.init()


class Background(object):
	def __init__(self, color):
		self.color = color
		update_queue.append(self)

	def update_screen(self):
		shop_display.fill(self.color)


class TextObject(object):
	def __init__(self, message, textx, texty, color, is_permanent, time_to_death):
		self.message = message
		self.textx = textx
		self.texty = texty
		self.color = color
		self.is_permanent = is_permanent
		self.time_to_death = time_to_death
		update_queue.append(self)

	def make_text(self):
		on_screen = font.render(self.message, True, self.color)
		shop_display.blit(on_screen, [self.textx, self.texty])

	def is_temp(self):
		if not self.is_permanent and self.time_to_death > 0:
			self.make_text()
			self.time_to_death -= 1
		if not self.is_permanent and self.time_to_death <= 0:
			update_queue.remove(self)

	def update_screen(self):
		self.is_temp()
		self.make_text()


class Shop(object):
	def __init__(self, name, greeting, items_for_sale, merchant_gold, in_shop):
		self.greeting = greeting
		self.name = name
		self.items_for_sale = items_for_sale
		self.merchant_gold = merchant_gold
		self.in_shop = in_shop
		self.shop_background = Background([0, 0, 0])
		self.shop_greeting = TextObject(self.greeting, 50, 50, (255, 255, 255), True, 0)
		self.shop_background.update_screen()
		self.shop_greeting.make_text()
		self.item_list = TextObject(self.items_for_sale, 75, 75, (255, 255, 255), True, 0)
		self.item_list.make_text()
		self.temp_greet = TextObject("Welcome to my shop!", 100, 187, (255, 255, 255), False, 3000)
		self.select_cursor = Cursor("shopcursor.png", 10, 75, 0)
		self.success_buy_temp = 0

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.in_shop = False
			if event.type == pygame.KEYDOWN:
				key = pygame.key.get_pressed()
				if key[pygame.K_ESCAPE]:
					self.in_shop = False
				if key[pygame.K_RETURN]:
					self.success_buy_temp = TextObject("Thank you for purchasing {}".format(self.items_for_sale), 50, 187, (255, 255, 255), False, 5000)
				if key[pygame.K_UP]:
					self.select_cursor.ychange = -25
					self.select_cursor.move_cursor()
				if key[pygame.K_DOWN]:
					self.select_cursor.ychange = 25
					self.select_cursor.move_cursor()

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
		self.ypos += 0.004	*(self.targetypos - self.ypos)
		self.xpos += 0.05 * sin(self.timer/10)


		display_image = pygame.image.load(self.image)
		shop_display.blit(display_image, [self.xpos, self.ypos])
		self.ychange = 0

	def move_cursor(self):
		self.targetypos += self.ychange

update_queue = []
shop_display = pygame.display.set_mode((400, 400))
font = pygame.font.SysFont(None, 25)
item_shop = Shop("Jay's Shop", "What would you like to buy?", "Potion", 2000, True)


while item_shop.in_shop:
	item_shop.handle_events()

pygame.quit()
quit()
'''
menuSelect = pygame.mixer.Sound("FF7ok.wav")
menuCancel = pygame.mixer.Sound("FF7cancel.wav")
menuWrong = pygame.mixer.Sound("FF7no.wav")
menuMove = pygame.mixer.Sound("FF7move.wav")

shopDisplay = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Welcome to Jay's shop!")
font = pygame.font.SysFont(None, 25)

potionPrice = 50
userGold = 100
merchantGold = 0
merchantPotionStock = 1

inShop = True


def displaytext(msg, textx, texty, color):
	on_screen = font.render(msg, True, color)
	shopDisplay.blit(on_screen, [textx, texty])


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


