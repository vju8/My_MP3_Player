from tkinter import filedialog  
from PIL import ImageTk, Image   
import tkinter as tk 
import pygame
import os 


    
class myMP3player(): 
    """
    The class for the MP3 Player.
    """
    def __init__(self):
        """
        myMP3Player constructor function where all the initial attributes 
        are being set. At the same time, the tkinter GUI is being initialized
        and filled with the needed widgets. To allow playing of the 
        MP3 files, pygame.mixer is used and initialized here. 

            Returns
            -------
            None.

        """
        self.root = tk.Tk()
        self.root.title("My MP3 Player")
        self.root.geometry("800x400")
        self.root.resizable(False, False)
        pygame.mixer.init() 
        self.root.protocol("WM_DELETE_WINDOW", lambda: [self.root.destroy(), pygame.mixer.quit()])
        self.root.bind('<Escape>', lambda e: [self.root.destroy(), pygame.mixer.quit()])
        
        self.app_title_frame = tk.Frame(self.root,
                                        bg = "#3D9140",
                                        height = 20)
        self.app_title_frame.pack(pady = 0, fill = tk.BOTH)
        self.app_title = tk.Label(self.app_title_frame,
                                  bg = "#3D9140",
                                  fg = "black",
                                  text = "My Mp3 Player",
                                  font = "Helvetica 30 bold") 
        self.app_title.pack(pady = 10) 
        
        self.menubar = tk.Menu(self.root)
        self.root.config(menu = self.menubar)
        self.organise_menu = tk.Menu(self.menubar, tearoff = False)   
        self.organise_menu.add_command(label = "Select Folder",
                                       command = self.load_music)
        self.menubar.add_cascade(label = "Browse", 
                                 menu = self.organise_menu)

        self.song_frame = tk.Frame(self.root,
                                 bg = "black",
                                 width = 600,
                                 height = 200)
        self.song_frame.pack(pady = 0, fill = tk.BOTH)
        self.song_frame.pack_propagate(0)    
        
        button_size = (80, 80)

        self.play_button_img = ImageTk.PhotoImage(Image.open("play_button.png").resize(button_size))
        self.pause_button_img = ImageTk.PhotoImage(Image.open("pause_button.png").resize(button_size))
        self.next_button_img = ImageTk.PhotoImage(Image.open("next_button.png").resize(button_size))
        self.previous_button_img = ImageTk.PhotoImage(Image.open("previous_button.png").resize(button_size))
        self.reset_button_img = ImageTk.PhotoImage(Image.open("reset_button.png").resize(button_size))

        self.control_frame = tk.Frame(self.root,
                                      bg = "white")
        self.control_frame.pack(pady = 20)

        self.play_pause_button = tk.Button(self.control_frame,
                                           image = self.play_button_img, 
                                           borderwidth = 0,
                                           command = self.play_pause_music)
        self.next_button = tk.Button(self.control_frame,
                                     image = self.next_button_img, 
                                     borderwidth = 0,
                                     command = self.next_music)
        self.previous_button = tk.Button(self.control_frame,
                                         image = self.previous_button_img, 
                                         borderwidth = 0,
                                         command = self.previous_music)
        self.reset_button = tk.Button(self.control_frame,
                                      image = self.reset_button_img, 
                                      borderwidth = 0,
                                      command = self.reset_music)
        
        self.play_pause_button.grid(row = 0, column = 1, padx = 10, pady = 0)
        self.next_button.grid(row = 0, column = 3, padx = 10, pady = 0)
        self.previous_button.grid(row = 0, column = 0, padx = 10, pady = 0)
        self.reset_button.grid(row = 0, column = 2, padx = 10, pady = 0)
        
        self.root.eval("tk::PlaceWindow . center")
        self.root.mainloop()
        
    def load_music(self):
        """
        Function responsible to load the list of songs from a chosen directory
        and displaying on the tkinter song frame the current song, the previous 
        song and the next song.

            Returns
            -------
            None.

        """
        self.songs = []
        self.current_song = ""
        self.playing = False
        self.same_song = False
        self.root.directory = filedialog.askdirectory()    
        for song in os.listdir(self.root.directory):       
            name, ext = os.path.splitext(song)             
            if ext == ".mp3":                              
                self.songs.append(song)
        
        self.song_idx = 0
        self.current_song = self.songs[self.song_idx]
        
        self.previous_song_label = tk.Label(self.song_frame,
                                             text = self.songs[-1],
                                             font = "Helvetica 12 bold",
                                             bg = "black",
                                             fg = "white")
            
        self.current_song_label = tk.Label(self.song_frame,
                                           text = self.current_song,
                                           font = "Helvetica 22 bold",
                                           bg = "black",
                                           fg = "white")
        
        self.next_song_label = tk.Label(self.song_frame,
                                        text = self.songs[self.song_idx + 1],
                                        font = "Helvetica 12 bold",
                                        bg = "black",
                                        fg = "white")
        
        self.previous_song_label.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
        self.current_song_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.next_song_label.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
        
    def play_pause_music(self):
        """
        Function responsible to play or pause a song. The image of the 
        play/pause button widget will change depending on setup. 

            Returns
            -------
            None.

        """
        if hasattr(self, "playing") == False:
            pass 
        else:
            if self.playing == False:
                if self.same_song == False:
                    pygame.mixer.music.load(os.path.join(self.root.directory, self.current_song))
                    pygame.mixer.music.play()  
                    
                    self.previous_song_label.config(text = self.songs[self.song_idx -1])
                    self.current_song_label.config(text = self.current_song)
                    self.next_song_label.config(text = self.songs[self.song_idx + 1])
                    
                else:
                    pygame.mixer.music.unpause()             
                
                self.play_pause_button.config(image = self.pause_button_img)
                self.playing = True  
            else:  
                pygame.mixer.music.pause()
                self.playing = False
                self.same_song = True
                self.play_pause_button.config(image = self.play_button_img)
            
            
    def next_music(self):
        """
        Function responsible to play the next song in the queue.

            Returns
            -------
            None.

        """
        if hasattr(self, "songs") == False:
            pass 
        else:
            try:
                self.song_idx += 1
                self.current_song = self.songs[self.song_idx]
                self.playing = False
                self.same_song = False
                self.play_pause_music()
            except:
                self.song_idx = 0
                self.current_song = self.songs[self.song_idx]
                self.playing = False
                self.same_song = False
                self.play_pause_music()

    def previous_music(self):
        """
        Function responsible to play the previous song in the queue.

            Returns
            -------
            None.

        """
        if hasattr(self, "songs") == False:
            pass 
        else:
            try:
                self.song_idx -= 1
                self.current_song = self.songs[self.song_idx]
                self.playing = False
                self.same_song = False
                self.play_pause_music()
            except:
                self.song_idx = -1
                self.current_song = self.songs[self.song_idx]
                self.playing = False
                self.same_song = False
                self.play_pause_music()
    
    def reset_music(self):
        """
        Function responsible to reset the current song (= get back to the 
        beginning of the song and pause).

            Returns
            -------
            None.

        """
        if hasattr(self, "playing") == False:
            pass 
        else:
            pygame.mixer.music.rewind()
            self.same_song = False
            self.playing = True
            self.play_pause_music()
    
    
mp3player = myMP3player()