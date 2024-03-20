import tkinter as tk
from tkinter import messagebox
from rubrica import RubricaGUI
import json

class Utente:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class FinestraLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self.root, text="Password:").grid(row=1, column=0, padx=5, pady=5)

        self.utenti_registrati = self.carica_utenti("utenti.txt")

        login_btn = tk.Button(self.root, text="LOGIN", command=self.verifica_login)
        login_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def carica_utenti(self, nome_file):
        try:
            with open(nome_file, "r") as file:
                utenti_registrati = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Errore! Non esiste il file!")
            utenti_registrati = {}
        return utenti_registrati

    def verifica_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.verifica_credenziali(username, password):
            self.root.destroy()
            finestra_principale = tk.Tk()
            app = RubricaGUI(finestra_principale)
            finestra_principale.mainloop()
        else:
            messagebox.showerror("Errore", "Login errato")

    def verifica_credenziali(self, username, password):
        if username in self.utenti_registrati and self.utenti_registrati[username] == password:
            return True
        else:
            return False

root_login = tk.Tk()
finestra_login = FinestraLogin(root_login)
root_login.mainloop()
