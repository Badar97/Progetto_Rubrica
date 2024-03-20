import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
from PIL import Image, ImageTk

class Persona:
    def __init__(self, nome, cognome, indirizzo, telefono, eta=0):
        self.nome = nome
        self.cognome = cognome
        self.indirizzo = indirizzo
        self.telefono = telefono
        self.eta = eta

class RubricaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rubrica Telefonica")

        self.persona_attuale = None
        self.persone = []

        self.crea_tabella()
        #self.crea_bottoni()
        self.crea_toolbar()
        self.carica_dati()

    def crea_tabella(self):
        self.table = ttk.Treeview(self.root, columns=('Nome', 'Cognome', 'Telefono', 'Indirizzo', 'Eta'))
        self.table.heading('#0', text='ID')
        self.table.heading('Nome', text='Nome')
        self.table.heading('Cognome', text='Cognome')
        self.table.heading('Indirizzo', text='Indirizzo')
        self.table.heading('Telefono', text='Telefono')
        self.table.heading('Eta', text='Eta')

        self.table.column('#0', width=100)
        self.table.column('Nome', width=100)
        self.table.column('Cognome', width=100)
        self.table.column('Telefono', width=100)
        self.table.column('Indirizzo', width=100)
        self.table.column('Eta', width=100)

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
    def crea_toolbar(self):
        self.toolbar = ttk.Frame(self.root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        nuovo_btn_img = Image.open("img/nuovo_icon.jpg").resize((20, 20), Image.ANTIALIAS)
        self.nuovo_btn_img = ImageTk.PhotoImage(nuovo_btn_img)
        nuovo_btn = ttk.Button(self.toolbar, image=self.nuovo_btn_img, command=self.apri_editor)
        nuovo_btn.grid(row=0, column=0, padx=5, pady=5)

        modifica_btn_img = Image.open("img/modifica_icon.png").resize((20, 20), Image.ANTIALIAS)
        self.modifica_btn_img = ImageTk.PhotoImage(modifica_btn_img)
        modifica_btn = ttk.Button(self.toolbar, image=self.modifica_btn_img, command=self.modifica_persona)
        modifica_btn.grid(row=0, column=1, padx=5, pady=5)

        elimina_btn_img = Image.open("img/elimina_icon.png").resize((20, 20), Image.ANTIALIAS)
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
        self.editor.destroy()

    def annulla_modifica(self):
        self.editor.destroy()

    def carica_dati(self):
        try:
            with open("informazioni.txt", "r") as file:
                for line in file:
                    data = line.strip().split(';')
                    nome = data[0]
                    cognome = data[1]
                    indirizzo = data[2]
                    telefono = data[3]
                    eta = int(data[4])
                    persona = Persona(nome, cognome, indirizzo, telefono, eta)
                    self.persone.append(persona)
            self.aggiorna_tabella()
        except FileNotFoundError:
            pass
    
    def salva_dati(self):
        with open("informazioni.txt", "w") as file:
            for persona in self.persone:
                file.write(f"{persona.nome};{persona.cognome};{persona.indirizzo};{persona.telefono};{persona.eta}\n")

    def salva_dati_mod(self):
        if not os.path.exists("informazioni"):
            os.makedirs("informazioni")
        for persona in self.persone:
            nome_file = f"{persona.nome}-{persona.cognome}.txt"
            cnt = 1
            while os.path.exists(os.path.join("informazioni", nome_file)):
                with open(os.path.join("informazioni", nome_file), "r") as file:
                    lines = file.readlines()
                    det = [line.strip().split(': ')[1] for line in lines[:3]]
                if det == [persona.indirizzo, persona.telefono, str(persona.eta)]:
                    break
                else:
                    nome_file = f"{persona.nome}-{persona.cognome}-{cnt}.txt"
                    cnt += 1
            with open(os.path.join("informazioni", nome_file), "w") as file:
                file.write(f"Nome: {persona.nome}\n")
                file.write(f"Cognome: {persona.cognome}\n")
                file.write(f"Indirizzo: {persona.indirizzo}\n")
                file.write(f"Telefono: {persona.telefono}\n")
                file.write(f"Eta: {persona.eta}\n")


#root = tk.Tk()
#app = RubricaGUI(root)
#root.mainloop()
