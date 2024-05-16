import pygame

#from playsound import playsound
#playsound(f'/home/ubuntu/pupper7/mitchell/sounds/{file}.mp3')


file = 'birds'

pygame.mixer.init()
pygame.mixer.music.load(f'/home/ubuntu/pupper7/mitchell/sounds/{file}.mp3')
pygame.mixer.music.play()