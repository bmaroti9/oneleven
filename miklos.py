import pygame

image = pygame.image.load("images/balck_and_white.png")
array = pygame.surfarray.array3d(image)

print(array.shape)
width, height, _ = array.shape

for x in range(min(width, height)):
    array[x, x, 0] = 255

clock = pygame.time.Clock()
surface = pygame.display.set_mode((width, height))
surface.blit(pygame.surfarray.make_surface(array), (0, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    pygame.display.update()
    clock.tick(40)
