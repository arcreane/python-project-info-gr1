import random

import tkinter as tk

from tkinter import messagebox


def melanger_mots(mot):
    lettres = list(mot)

    random.shuffle(lettres)

    return ''.join(lettres)


def verifier_reponse():
    global essais, mot_correct

    reponse = entry.get().strip().lower()

    if reponse == mot_correct:

        messagebox.showinfo("Victoire du Capitaine !", "Par les sept mers ! Tu as trouvé l’code ! Le coffre s’ouvre !")

        root.destroy()

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


def jouer():
    global essais, mot_correct, entry, label_info, root

    mots_pirates = ["carte", "trésor", "pirate", "boussole", "capitaine", "sabre"]

    mot_correct = random.choice(mots_pirates)

    mot_melange = melanger_mots(mot_correct)

    essais = 3

    root = tk.Tk()

    root.title("⚓ Le Code du Capitaine ⚓")

    root.geometry("420x320")

    root.resizable(False, False)

    root.configure(bg="#f2e6c9")

    label_titre = tk.Label(root, text="🏴‍☠️ Le Code du Capitaine 🏴‍☠️",

                           font=("Papyrus", 18, "bold"), bg="#f2e6c9", fg="#4b3621")

    label_titre.pack(pady=10)

    label_instruction = tk.Label(root, text=f"Gravure ancienne : {mot_melange}",

                                 font=("Courier", 16), bg="#f2e6c9", fg="#1e1e1e")

    label_instruction.pack(pady=10)

    entry = tk.Entry(root, font=("Courier", 16), justify='center')

    entry.pack(pady=5)

    bouton_valider = tk.Button(root, text="🔐 Réciter l’incantation",

                               font=("Courier", 14, "bold"), bg="#d4af37", command=verifier_reponse)

    bouton_valider.pack(pady=10)

    label_info = tk.Label(root, text="", font=("Arial", 12), fg="crimson", bg="#f2e6c9")

    label_info.pack(pady=10)

    root.mainloop()


# Lancer le jeu

if __name__ == "__main__":
    jouer()