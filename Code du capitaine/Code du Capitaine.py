import random

import tkinter as tk

from tkinter import messagebox


def melanger_mots(mot):
    lettres = list(mot)

    random.shuffle(lettres)

    return ''.join(lettres)


def verifier_reponse():
    global essais, mot_correct, victoires_consecutives

    reponse = entry.get().strip().lower()

    if reponse == mot_correct:

        victoires_consecutives += 1

        if victoires_consecutives == 3:

            messagebox.showinfo("Victoire du Capitaine !",

                                "Par les sept mers ! Trois codes déchiffrés ! Le coffre s’ouvre enfin !")

            root.destroy()

        else:

            messagebox.showinfo("Bravo moussaillon !",

                                f"Correct ! Encore {3 - victoires_consecutives} code(s) à percer.")

            lancer_nouveau_mot()

    else:

        essais -= 1

        if essais > 0:

            label_info.config(

                text=f"Argh ! Mauvaise incantation. Encore {essais} tentative(s), moussaillon !")

            entry.delete(0, tk.END)

        else:

            messagebox.showerror("Échec du Pirate",

                                 f"Le sort est lancé... Le bon mot était '{mot_correct}'. Le trésor reste caché.")

            root.destroy()


def lancer_nouveau_mot():
    global mot_correct, essais

    mot_correct = random.choice(mots_pirates)

    mot_melange = melanger_mots(mot_correct)

    label_instruction.config(text=f"Gravure ancienne : {mot_melange}")

    entry.delete(0, tk.END)

    essais = 3

    label_info.config(text="")


def jouer():
    global essais, mot_correct, entry, label_info, root, mots_pirates, label_instruction, victoires_consecutives

    mots_pirates = ["carte", "trésor", "pirate", "boussole", "capitaine", "sabre"]

    victoires_consecutives = 0

    essais = 3

    root = tk.Tk()

    root.title("⚓ Le Code du Capitaine ⚓")

    root.geometry("420x320")

    root.resizable(False, False)

    root.configure(bg="#f2e6c9")

    label_titre = tk.Label(root, text="🏴‍☠️ Le Code du Capitaine 🏴‍☠️",

                           font=("Papyrus", 18, "bold"), bg="#f2e6c9", fg="#4b3621")

    label_titre.pack(pady=10)

    label_instruction = tk.Label(root, font=("Courier", 16), bg="#f2e6c9", fg="#1e1e1e")

    label_instruction.pack(pady=10)

    entry = tk.Entry(root, font=("Courier", 16), justify='center')

    entry.pack(pady=5)

    bouton_valider = tk.Button(root, text="🔐 Réciter l’incantation",

                               font=("Courier", 14, "bold"), bg="#d4af37", command=verifier_reponse)

    bouton_valider.pack(pady=10)

    label_info = tk.Label(root, text="", font=("Arial", 12), fg="crimson", bg="#f2e6c9")

    label_info.pack(pady=10)

    lancer_nouveau_mot()

    root.mainloop()


# Lancer le jeu

if __name__ == "__main__":
    jouer()