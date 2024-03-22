import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os

import mysql.connector
from mysql.connector import Error
import configparser

class Persona:
    def __init__(self, nome, cognome, indirizzo, telefono, eta=0):
        self.nome = nome
        self.cognome = cognome
        self.indirizzo = indirizzo
        self.telefono = telefono
        self.eta = eta

class Scanner:
    def __init__(self, file_path):
        self.file_path = file_path

    def leggi_file(self):
        try:
            with open(self.file_path, 'r') as file:
                file_content = file.read()
                return file_content
        except FileNotFoundError:
            messagebox.showinfo('Info', f"Il file '{self.file_path}' non è stato trovato.")
            return None
        except Exception as e:
            messagebox.showerror('Errore', f"Si è verificato un errore durante la lettura del file: {e}")
            return None

class PrintStream:
    def __init__(self, filename):
        try:
            self.file = open(filename, "w")
        except IOError:
            messagebox.showerror('Errore', "Errore durante l'apertura del file")
    
    def println(self, text):
        print(text, file=self.file)
    
    def close(self):
        self.file.close()

class RubricaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rubrica Telefonica")

        self.persona_attuale = None
        self.persone = []

        self.crea_tabella()
        #self.crea_bottoni()
        self.crea_toolbar_btn()
        self.conn = self.connetti_database()
        if self.conn:
            print("Connessione al database avvenuta con successo!")
            self.cursor = self.conn.cursor()
            self.crea_database()
            self.carica_dati()

        self.root.protocol("WM_DELETE_WINDOW", self.chiusura_database)

    def connetti_database(self):
        try:
            config = configparser.ConfigParser()
            config.read('credenziali_database.properties')
            username = config.get('database', 'username')
            password = config.get('database', 'password')
            hostname = config.get('database', 'hostname')
            porta = config.get('database', 'porta')
            #database = config.get('database', 'database')
            conn = mysql.connector.connect(
                host=hostname,
                port=porta,
                user=username,
                password=password
                #db=database
            )
            return conn
        except Error as e:
            print(f"Errore di connessione al database: {e}")
            return None
    
    def chiusura_database(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("Chiusura del database avvenuta con successo!")
        self.root.destroy()

    """
    def crea_database(self):
        try:
            with open('schema_database.sql', 'r') as file:
                script_sql = file.read()
                self.cursor.execute(script_sql, multi=True)
                #self.cursor.fetchall()
                #self.conn.commit()
                print("database creato")
        except Error as e:
            print(f"Errore durante l'esecuzione dello script SQL: {e}")
    """
    def crea_database(self):
        try:
            with open('schema_database.sql', 'r') as file:
                script_sql = file.read()
                queries = script_sql.split(';')  # Dividi le query separate dal punto e virgola
                for query in queries:
                    query = query.strip()
                    if query:  # Ignora le stringhe vuote
                        self.cursor.execute(query)
                self.conn.commit()
                print("Database e tabella create con successo!")
        except Error as e:
            print(f"Errore durante l'esecuzione dello script SQL: {e}")

    
    def salva_dati_db(self):
        try:
            for persona in self.persone:
                insert_query = """INSERT INTO persone (nome, cognome, indirizzo, telefono, eta)
                VALUES (%s, %s, %s, %s, %s)"""
                data = (persona.nome, persona.cognome, persona.indirizzo, persona.telefono, persona.eta)
                self.cursor.execute(insert_query, data)
                #self.cursor.close()
            #self.cursor.fetchall()
            self.conn.commit()
            print("Dati salvati nel database con successo!")
        except Error as e:
            print(f"Errore durante il salvataggio dei dati nel database: {e}")

    def crea_tabella(self):
        self.table = ttk.Treeview(self.root, columns=('Nome', 'Cognome', 'Telefono'))
        self.table.heading('#0', text='ID')
        self.table.heading('Nome', text='Nome')
        self.table.heading('Cognome', text='Cognome')
        #self.table.heading('Indirizzo', text='Indirizzo')
        self.table.heading('Telefono', text='Telefono')
        #self.table.heading('Eta', text='Eta')

        self.table.column('#0', width=100)
        self.table.column('Nome', width=100)
        self.table.column('Cognome', width=100)
        #self.table.column('Indirizzo', width=100)
        self.table.column('Telefono', width=100)
        #self.table.column('Eta', width=100)

        self.table.pack(padx=5, pady=5)

    def aggiorna_tabella(self):
        self.table.delete(*self.table.get_children())
        for i, persona in enumerate(self.persone):
            self.table.insert('', 'end', text=str(i), values=(persona.nome, persona.cognome, persona.indirizzo, persona.telefono, persona.eta))

    """
    def crea_bottoni(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        nuovo_btn = tk.Button(frame, text="Nuovo", command=self.apri_editor)
        nuovo_btn.grid(row=0, column=0, padx=5)

        modifica_btn = tk.Button(frame, text="Modifica", command=self.modifica_persona)
        modifica_btn.grid(row=0, column=1, padx=5)

        elimina_btn = tk.Button(frame, text="Elimina", command=self.elimina_persona)
        elimina_btn.grid(row=0, column=2, padx=5)
    """
    def crea_toolbar_btn(self):
        self.toolbar = ttk.Frame(self.root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        nuovo_btn_img = Image.open("img/nuovo_icon.jpg").resize((20, 20), Image.Resampling.LANCZOS)
        self.nuovo_btn_img = ImageTk.PhotoImage(nuovo_btn_img)
        nuovo_btn = ttk.Button(self.toolbar, image=self.nuovo_btn_img, command=self.apri_editor)
        nuovo_btn.grid(row=0, column=0, padx=5, pady=5)

        modifica_btn_img = Image.open("img/modifica_icon.png").resize((20, 20), Image.Resampling.LANCZOS)
        self.modifica_btn_img = ImageTk.PhotoImage(modifica_btn_img)
        modifica_btn = ttk.Button(self.toolbar, image=self.modifica_btn_img, command=self.modifica_persona)
        modifica_btn.grid(row=0, column=1, padx=5, pady=5)

        elimina_btn_img = Image.open("img/elimina_icon.png").resize((20, 20), Image.Resampling.LANCZOS)
        self.elimina_btn_img = ImageTk.PhotoImage(elimina_btn_img)
        elimina_btn = ttk.Button(self.toolbar, image=self.elimina_btn_img, command=self.elimina_persona)
        elimina_btn.grid(row=0, column=2, padx=5, pady=5)

    def apri_editor(self):
        self.editor = tk.Toplevel(self.root)
        self.editor.title("Editor Persona")

        tk.Label(self.editor, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self.editor, text="Cognome:").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(self.editor, text="Indirizzo:").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(self.editor, text="Telefono:").grid(row=3, column=0, padx=5, pady=5)
        tk.Label(self.editor, text="Eta:").grid(row=4, column=0, padx=5, pady=5)

        self.nome_entry = tk.Entry(self.editor)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)
        self.cognome_entry = tk.Entry(self.editor)
        self.cognome_entry.grid(row=1, column=1, padx=5, pady=5)
        self.indirizzo_entry = tk.Entry(self.editor)
        self.indirizzo_entry.grid(row=2, column=1, padx=5, pady=5)
        self.telefono_entry = tk.Entry(self.editor)
        self.telefono_entry.grid(row=3, column=1, padx=5, pady=5)
        self.eta_entry = tk.Entry(self.editor)
        self.eta_entry.grid(row=4, column=1, padx=5, pady=5)

        save_btn = tk.Button(self.editor, text="Salva", command=self.salva_persona)
        save_btn.grid(row=5, column=0, columnspan=2, pady=5)

        annulla_btn = tk.Button(self.editor, text="Annulla", command=self.annulla_modifica)
        annulla_btn.grid(row=6, column=0, columnspan=2, pady=5)

        if self.persona_attuale:
            self.nome_entry.insert(0, self.persona_attuale.nome)
            self.cognome_entry.insert(0, self.persona_attuale.cognome)
            self.indirizzo_entry.insert(0, self.persona_attuale.indirizzo)
            self.telefono_entry.insert(0, self.persona_attuale.telefono)
            self.eta_entry.insert(0, self.persona_attuale.eta)

    def modifica_persona(self):
        selected_item = self.table.selection()
        if selected_item:
            index = int(self.table.item(selected_item)['text'])
            self.persona_attuale = self.persone[index]
            self.apri_editor()
        else:
            messagebox.showerror("Errore", "Seleziona prima una persona da modificare.")

    def elimina_persona(self):
        selected_item = self.table.selection()
        if selected_item:
            index = int(self.table.item(selected_item)['text'])
            persona = self.persone[index]
            conferma = messagebox.askquestion("Conferma", f"Eliminare la persona {persona.nome} {persona.cognome}?")
            if conferma == 'yes':
                del self.persone[index]
                self.aggiorna_tabella()
                self.salva_dati()
                self.salva_dati_mod()
        else:
            messagebox.showerror("Errore", "Seleziona prima una persona da eliminare.")

    def salva_persona(self):
        nome = self.nome_entry.get()
        cognome = self.cognome_entry.get()
        indirizzo = self.indirizzo_entry.get()
        telefono = self.telefono_entry.get()
        eta = self.eta_entry.get()

        if self.persona_attuale:
            self.persona_attuale.nome = nome
            self.persona_attuale.cognome = cognome
            self.persona_attuale.indirizzo = indirizzo
            self.persona_attuale.telefono = telefono
            self.persona_attuale.eta = eta
            self.persona_attuale = None
        else:
            persona = Persona(nome, cognome, indirizzo, telefono, eta)
            self.persone.append(persona)

        self.aggiorna_tabella()
        self.salva_dati()
        self.salva_dati_mod()
        self.salva_dati_db()
        self.editor.destroy()

    def annulla_modifica(self):
        self.editor.destroy()

    def carica_dati(self):
        try:
            file_reader = Scanner("informazioni.txt")
            file_content = file_reader.leggi_file()
            if file_content:
                lines = file_content.split('\n')
                for line in lines:
                    data = line.split(';')
                    if len(data) >= 5:
                        nome = data[0]
                        cognome = data[1]
                        indirizzo = data[2]
                        telefono = data[3]
                        eta = int(data[4])
                        persona = Persona(nome, cognome, indirizzo, telefono, eta)
                        self.persone.append(persona)
                self.aggiorna_tabella()
        except Exception as e:
            messagebox.showerror('Errore', f"Si è verificato un errore durante il caricamento dei dati: {e}")

    
    def salva_dati(self):
        try:
            print_stream = PrintStream("informazioni.txt")
            for persona in self.persone:
                print_stream.println(f"{persona.nome};{persona.cognome};{persona.indirizzo};{persona.telefono};{persona.eta}")
            print_stream.close()
        except FileNotFoundError:
            pass

    def salva_dati_mod(self):
        try:
            if not os.path.exists("informazioni"):
                os.makedirs("informazioni")
            for persona in self.persone:
                nome_file_base = f"{persona.nome}-{persona.cognome}.txt"
                nome_file = nome_file_base
                cnt = 1
                while os.path.exists(os.path.join("informazioni", nome_file)):
                    with open(os.path.join("informazioni", nome_file), "r") as file:
                        lines = file.readlines()
                        det = [line.strip().split(': ')[1] for line in lines[-3:]]
                    if det == [persona.indirizzo, persona.telefono, str(persona.eta)]:
                        break
                    else:
                        nome_file = f"{persona.nome}-{persona.cognome}-{cnt}.txt"
                        cnt += 1
                print_stream = PrintStream(os.path.join("informazioni", nome_file))
                print_stream.println(f"Nome: {persona.nome}")
                print_stream.println(f"Cognome: {persona.cognome}")
                print_stream.println(f"Indirizzo: {persona.indirizzo}")
                print_stream.println(f"Telefono: {persona.telefono}")
                print_stream.println(f"Eta: {persona.eta}")
            messagebox.showinfo("Info", "Dati salvati in file nella cartella 'informazioni'")
        except FileNotFoundError:
            pass
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

        #self.utenti_registrati = self.carica_utenti("utenti.txt")
        self.utenti_registrati = {
            "admin": "password",
            "user1": "1234",
            "root": ""
        }

        login_btn = tk.Button(self.root, text="LOGIN", command=self.verifica_login)
        login_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    
    """
    def carica_utenti(self, nome_file):
        try:
            with open(nome_file, "r") as file:
                utenti_registrati = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Errore",  "Non esiste il file")
            utenti_registrati = {}
        return utenti_registrati
    """

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

#root = tk.Tk()
#app = RubricaGUI(root)
#root.mainloop()
