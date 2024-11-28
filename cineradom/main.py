import customtkinter as ctk
from tkinter import filedialog
from random import shuffle
import vlc,os

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cineradom")
        self.geometry("1200x700")  # Taille de la fenêtre principale
        #self.resizable(False,False)

        # Configuration des colonnes pour un partage 75%-25%
        self.grid_columnconfigure(0, weight=3)  # 75% pour la colonne 0
        self.grid_columnconfigure(1, weight=1)  # 25% pour la colonne 1

        # Configuration des lignes
        self.grid_rowconfigure(0, weight=0)  # Ligne pour la frame supérieure (fixe)
        self.grid_rowconfigure(1, weight=1)  # Ligne pour les frames principales (75%-25%)

        # Initialisation du lecteur VLC
        self.vlc_instance = None
        self.vlc_player = None
        self.vlc_frame = None
        self.viewer = None  # Déclarer ici pour l'accès dans d'autres méthodes

        # Ajout des frames
        self.top_frame()    # Frame au-dessus
        self.main_frame()   # Frame principale (75%)
        self.right_frame()  # Frame de droite (25%)
        #self.add_vlc_player() #demander à lire un film dès le lancement

   
    def clean_frame(self, frame):
        """Détruit tous les widgets dans un cadre donné"""
        if not hasattr(frame, "winfo_children"):
            raise AttributeError(f"'{frame}' n'est pas un widget valide")
        
        for child in frame.winfo_children():
            child.destroy()

    def select(self,segment):#pour la topbar 
        """choisir la commande à executer"""

        chose={
            "lire":self.add_vlc_player,
            "playlist":self.listing,
            "paramètre":self.parametre,
            "aleatoire":self.random_movie,
            "historique":self.historique,
            "apropos":self.about
        }
        #je sais je sais ,je suis nul en anglais 0😂🤣
        for i in chose.keys():
            if i==segment:
                command=chose[i]()
                break
        return command
    
    #gere la topbar et compagnie
    def top_frame(self):
        """Frame supérieure (au-dessus des deux autres frames)"""
        top = ctk.CTkFrame(self, height=100, fg_color="gray")
        top.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")  # Occupe les deux colonnes
     
        
        topbar=ctk.CTkSegmentedButton(top,
                                      values=["lire","playlist","aleatoire","historique","paramètre","apropos"],
                                      unselected_color="blue",
                                      command=self.select)
        topbar.pack(fill="both",side='top')

    #gere la lecture de fichier
    def main_frame(self):
        """Frame principale (75% de la largeur)"""
        self.viewer = ctk.CTkFrame(self, width=600, height=580)#viewer est la boite utiliser pour la lecture de fichier
        self.viewer.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")  # Ligne 1, colonne 0
        msg=ctk.CTkLabel(self.viewer,
                         text="cineradom\n Appuyez sur le bouton lire et vivez une experience inoubliable😊👌",
                          font=("Arial", 20))
        msg.pack(expand=True,fill="both")

    def add_vlc_player(self):
        """Intégrer VLC dans main_frame"""
        if self.vlc_player and self.vlc_player.is_playing():
            self.vlc_player.stop()

        # Nettoyer l'écran
        self.clean_frame(self.viewer)

        # Créer un conteneur pour VLC (peut être un frame Tkinter natif pour le handle)
        self.vlc_frame = ctk.CTkFrame(self.viewer, width=600, height=500)
        self.vlc_frame.pack(fill="both", expand=True)

        # Créer une instance VLC si elle n'existe pas encore
        if not self.vlc_instance:
            self.vlc_instance = vlc.Instance()

        if not self.vlc_player:
            self.vlc_player = self.vlc_instance.media_player_new()

        # Obtenir le handle de la fenêtre pour dessiner la vidéo
        if hasattr(self.vlc_player, 'set_hwnd'):  # Windows
            self.vlc_player.set_hwnd(self.vlc_frame.winfo_id())
        else:  # MacOS / Linux
            self.vlc_player.set_xwindow(self.vlc_frame.winfo_id())

        # Charger un fichier vidéo
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers multimédias", "*.mp4 *.mp3 *.avi *.mkv *.flv *.mov *.wmv")])
        if not file_path:
            return  # Si aucun fichier n'est sélectionné, on ne continue pas

        media = self.vlc_instance.media_new(file_path)
        self.vlc_player.set_media(media)

        #ajouter le film ouvert dans le fichier d'historique
        with open("data/historique.txt","+a") as file:
            file.write(f'{file_path}\n')

        # Démarrer la lecture
        self.vlc_player.play()

    def right_frame(self):
        """Frame de droite (25% de la largeur)"""

        self.width=200#pour rendre les ecrits dynamique
        self.r_frame = ctk.CTkFrame(self, width=self.width, height=400)
        self.r_frame.grid(row=1, column=1, padx=10, pady=20, sticky="nsew")  # Ligne 1, colonne 1

        return self.frame
##_____________________________________________
    def parametre(self):
        """gere les parametre d'utilisation"""

        self.clean_frame(self.r_frame)
        msg=ctk.CTkLabel(self.r_frame,
                            text="Parametre\n ",
                            font=("Arial", 12))
        msg.pack(expand=True,fill="both")

#_____________________________________________

    def about(self):
        """nettoyer l'ecran """

        self.clean_frame(self.r_frame)

        label=ctk.CTkLabel(self.r_frame,
                            text="A propos \n cineradom est un logiciel de lecture multimedia Lorem ipsum dolor sit amet consectetur adipisicing elit. Iusto dignissimos, harum sit officia nulla assumenda eaque! Corrupti reiciendis consectetur recusandae repellat aut ex, enim tempora doloremque, aliquid veniam quibusdam. Temporibus.\n praise MAster de coeur ",
                            wraplength=self.width-20)
        
        label.pack(expand=True,fill="both",side="top")

##_____________________________________________
    def historique(self):
        self.clean_frame(self.r_frame)

        label=ctk.CTkLabel(self.r_frame,
                           text="historique de lecture",
                           font=("arial",16))
        label.pack()

        with open ("data/historique.txt",'r+') as file:
            data=file.readlines()
        for i in data:
            movie=i.split('/')
            name=movie[len(movie)-1].strip('\n')
            msg=ctk.CTkLabel(self.r_frame,
                            text=name,
                            font=("Arial", 12))
            msg.pack()

##_____________________________________________
    def listing(self):

        self.clean_frame(self.r_frame)

        msg=ctk.CTkLabel(self.r_frame,
                         text="cineradom\n playlist",
                          font=("Arial", 16))
        msg.pack(expand=True,fill="both")

    def playing_alea(self,movie):
        """lire la video choisi par l'utilisateur"""

        try:
            if self.vlc_player and self.vlc_player.is_playing():
                self.vlc_player.stop()

                media = self.vlc_instance.media_new(movie)
                self.vlc_player.set_media(movie)

                #commencer la lecture
                self.vlc_player.play()

        except:
            print("error")
            

    def random_movie(self):
        """choisire les film"""
        self.clean_frame(self.r_frame)

        repertoire=filedialog.askdirectory()
        small_list=list()
        extension=[".mp4",".avi"]
        
        if repertoire:
            row=0
            ctk.CTkButton(self.r_frame,text="films proposés :",font=("arial-bold",16),state="disable",text_color="black").grid(row=row, column=0,padx=0, pady=0,sticky="nwes")

            if os.listdir(repertoire):
                liste_film=[film for film in os.listdir(repertoire) if os.path.splitext(film)[1] in extension]
                shuffle(liste_film)

                for i in range(1,6):
                    small_list.append(liste_film[i])

                for film in small_list:
                    row+=1
                    ctk.CTkButton(self.r_frame,text=film,command=lambda:self.playing_alea(film)).grid(row=row, column=0,padx=0, pady=0,sticky="nwes")
            else:
                print('error')

            btn=ctk.CTkButton(self.r_frame,text="relancer",fg_color="green",command=self.random_movie).grid(row=row+1, column=0, padx=15, pady=15,sticky="nwes")

        #en cas d'erreur
        else:ctk.CTkLabel(self.r_frame,text="le repertoire est vide ou une erreur s'est produite !")


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Mode sombre
    ctk.set_default_color_theme("blue")  # Thème par défaut
    app = MyApp()
    app.mainloop()





        

    
