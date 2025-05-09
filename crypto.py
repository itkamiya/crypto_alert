import tkinter as tk
from tkinter import messagebox
import requests
import time

# Clé API CoinAPI
#API_KEY = ""
API_KEY = ""

# Fonction pour vérifier si le seuil est dépassé
def check_threshold():
    for index, item in enumerate(listbox_data.get(0, tk.END)):
        elements = item.split(",")
        if len(elements) != 3:
            print(f"La ligne {index + 1} ne contient pas les informations nécessaires.")
            continue
        
        crypto_name, threshold, type_price = elements
        url = f"https://rest.coinapi.io/v1/exchangerate/{crypto_name}/USD"
        headers = {"X-CoinAPI-Key": API_KEY}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            current_price = data["rate"]
            print(f"la crypto {crypto_name} est actuellement de : {current_price}")
            if (type_price.strip() == "lower_than" and current_price < float(threshold)) or \
               (type_price.strip() == "higher_than" and current_price > float(threshold)):
                # Affichage d'une alerte
                messagebox.showinfo("Alerte Crypto", f"La crypto {crypto_name} a dépassé le seuil!")
                # Supprimer l'élément de la liste
                listbox_data.delete(index)
        else:
            print(f"Impossible de récupérer les données pour {crypto_name}")
    # Attendre une seconde avant de rappeler la fonction
    root.after(10000, check_threshold)

# Fonction pour ajouter les données saisies à la liste
def submit_form():
    nom_crypto = entry_nom_crypto.get()
    prix_crypto = entry_prix_crypto.get()
    select_value = select_type_prix.get()
    
    # Ajout des données à la liste
    listbox_data.insert(tk.END, f"{nom_crypto}, {prix_crypto}, {select_value}")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Suivi Crypto")

# Création des libellés et des zones de saisie pour chaque champ
label_nom_crypto = tk.Label(root, text="Nom de la crypto:")
label_nom_crypto.grid(row=0, column=0, padx=5, pady=5)
entry_nom_crypto = tk.Entry(root)
entry_nom_crypto.grid(row=0, column=1, padx=5, pady=5)

label_prix_crypto = tk.Label(root, text="Prix de la crypto:")
label_prix_crypto.grid(row=1, column=0, padx=5, pady=5)
entry_prix_crypto = tk.Entry(root)
entry_prix_crypto.grid(row=1, column=1, padx=5, pady=5)

label_select_type_prix = tk.Label(root, text="Sélectionnez le type de prix:")
label_select_type_prix.grid(row=2, column=0, padx=5, pady=5)
select_type_prix = tk.StringVar(root)
select_type_prix.set("lower_than")
select = tk.OptionMenu(root, select_type_prix, "lower_than", "higher_than")
select.grid(row=2, column=1, padx=5, pady=5)

# Bouton de soumission
submit_button = tk.Button(root, text="Soumettre", command=submit_form)
submit_button.grid(row=3, columnspan=2, padx=5, pady=10)

# Liste pour afficher les données saisies
listbox_data = tk.Listbox(root)
listbox_data.grid(row=4, columnspan=2, padx=5, pady=5, sticky="nsew")

# Configuration de l'extension de la liste pour qu'elle remplisse tout l'espace disponible
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(0, weight=1)

# Démarrer la vérification du seuil
check_threshold()

# Boucle principale de l'application
root.mainloop()
