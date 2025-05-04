import pygame
import random
import time
import sys

pygame.init()

# création fenêtre
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Le Coffre du Pirate")


# fonction fond d'écran
def load_background():
    try:
        background = pygame.image.load('Fond/ile.png')
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Adapter à la taille de la fenêtre
        return background
    except pygame.error:
        print("Erreur : impossible de charger le fond d'écran")
        sys.exit()


background = load_background()

# Police
FONT = pygame.font.SysFont("Papyrus", 50)  # Police normale sans gras
SMALL_FONT = pygame.font.SysFont("Papyrus", 30)  # Police normale pour texte plus petit

# Couleurs format RGB
WHITE = (255, 255, 255)
GOLD = (255, 202, 0)

# Lettres possibles
LETTERS = [chr(i) for i in range(65, 91)]  # A-Z

# Modalité des tours
TOURS = [
    (6, 15),
    (7, 16),
    (8, 17),
    (9, 18),
    (10, 19)
]


# Fonction bouton
def draw_button(text, x, y, w, h):
    pygame.draw.rect(WIN, WHITE, (x, y, w, h))  # couleur du bouton
    label = SMALL_FONT.render(text, True, GOLD)  # texte du bouton
    WIN.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))  # Centre le texte
    return pygame.Rect(x, y, w, h)


# Affiche messages (texte centré)
def show_message(message, text_color, x, y):
    text_surface = FONT.render(message, True, text_color)
    text_rect = text_surface.get_rect(center=(x, y))

    # Afficher texte
    WIN.blit(text_surface, (text_rect.x, text_rect.y))

    pygame.display.update()


# Affiche temps restant
def display_sequence_with_timer(sequence, duration):
    start_time = time.time()
    clock = pygame.time.Clock()

    while True:
        elapsed = time.time() - start_time
        remaining = max(0, int(duration - elapsed))
        if elapsed >= duration:
            break

        WIN.blit(background, (0, 0))  # fond

        # Affiche séquence de lettres
        text = ' '.join(sequence)
        text_surface = FONT.render(text, True, GOLD)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        WIN.blit(text_surface, (text_rect.x, text_rect.y))

        # Affiche le chrono
        timer_label = SMALL_FONT.render(f"Temps restant : {remaining} sec", True, GOLD)
        WIN.blit(timer_label, ((WIDTH - timer_label.get_width()) // 2, HEIGHT // 2 + 40))

        pygame.display.update()
        clock.tick(30)


# Saisie utilisateur
def input_sequence(length):
    user_input = ""
    clock = pygame.time.Clock()
    active = True
    cursor_visible = True
    cursor_timer = 0
    CURSOR_INTERVAL = 500  # vitesse du clignotement en ms


    input_box = pygame.Rect(WIDTH // 2 - 250, 200, 500, 80)  # Largeur = 500, Hauteur = 80

    while active:
        WIN.blit(background, (0, 0))  # Afficher le fond avant chaque interaction

        # Affiche texte
        prompt = SMALL_FONT.render("Tape ta réponse:", True, GOLD)
        WIN.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 120))

        # curseur clignotant
        current_time = pygame.time.get_ticks()
        if current_time - cursor_timer > CURSOR_INTERVAL:
            cursor_visible = not cursor_visible
            cursor_timer = current_time

        # zone de saisie
        pygame.draw.rect(WIN, WHITE, input_box)
        pygame.draw.rect(WIN, GOLD, input_box, 2)

        # Affiche le texte saisi
        text_surface = FONT.render(user_input, True, GOLD)
        WIN.blit(text_surface, (input_box.x + 10, input_box.y + 10))

        # Curseur
        if cursor_visible:
            cursor_x = input_box.x + 10 + text_surface.get_width()
            cursor_y = input_box.y + 10
            pygame.draw.line(WIN, GOLD, (cursor_x, cursor_y), (cursor_x, cursor_y + text_surface.get_height()), 2)

        # Bouton de validation
        validate_btn = draw_button("Valider", WIDTH // 2 - 100, 300, 200, 60)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    return user_input.upper()
                elif event.unicode.isalpha() and len(user_input) < length:
                    user_input += event.unicode.upper()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if validate_btn.collidepoint(event.pos):
                    return user_input.upper()

        clock.tick(30)


# Écran de menu
def menu():
    run = True
    clock = pygame.time.Clock()  # Ajout d'un objet clock pour contrôler la vitesse de rafraîchissement
    while run:
        WIN.blit(background, (0, 0))  # fond

        # Affiche titre et texte
        show_message("Le Coffre du Pirate", GOLD, WIDTH // 2, HEIGHT // 3)
        show_message("Commencer la partie ?", GOLD, WIDTH // 2, HEIGHT // 2)

        # Bouton de démarage
        start_button = draw_button("Démarrer", WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 60)

        pygame.display.update()

        # ralenti pb de clignotement du bouton
        clock.tick(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    run = False  # Fermer le menu et démarrer le jeu


# Affiche un message et attend un clic pour avancer
def wait_for_click(message):
    WIN.blit(background, (0, 0))  # Réafficher le fond
    show_message(message, GOLD, WIDTH // 2, HEIGHT // 2)  # Message centré sur l'écran
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False  # Quitter la boucle et avancer


# Jeu
def main():
    menu()  # Affiche le menu

    run = True
    tour = 0
    used_retry = False

    while tour < len(TOURS):
        sequence_len, display_time = TOURS[tour]
        sequence = random.sample(LETTERS, sequence_len)

        while True:
            display_sequence_with_timer(sequence, display_time)
            wait_for_click("Tu as bien tout retenu ?(clique)")  # Attendre un clic avant de continuer


            guess = input_sequence(sequence_len)

            if guess == ''.join(sequence):

                wait_for_click("Bravo ! (clique)")  # Attendre un clic pour la prochaine action

                tour += 1
                break
            else:
                if not used_retry:
                    wait_for_click("Raté !(clique)")  # Attendre un clic
                    retry_btn = draw_button("Nouvelle manche", WIDTH // 2 - 100, HEIGHT // 2 + 60, 215, 55)
                    pygame.display.update()
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                if retry_btn.collidepoint(event.pos):
                                    used_retry = True
                                    waiting = False
                    continue  # relance le tour avec une nouvelle séquence
                else:
                    wait_for_click("Raté ! Recommence depuis le début")  # Attendre un clic
                    tour = 0
                    used_retry = False
                    break

    wait_for_click("Bravo ! Tu as gagné les 5 manches !")  # Attendre un clic pour finir
    pygame.quit()


if __name__ == "__main__":
    main()
