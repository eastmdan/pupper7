import pygame

#from playsound import playsound

#

#file = 'birds'

#
#playsound(f'/home/ubuntu/pupper7/mitchell/sounds/{file}.mp3')


pygame.mixer.init()
pygame.mixer.music.load(f'/home/ubuntu/pupper7/mitchell/sounds/{file}.mp3')
pygame.mixer.music.play()