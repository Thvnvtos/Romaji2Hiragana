import tkinter as tk


# Dictionnaries to link between Romaji and unicode for Hiragana characters:
H_size1 = {'a':0x3042,'i':0x3044,'u':0x3046,'e':0x3048,'o':0x304A,'n':0x3093} # dictionnary for  size 1 Hiragana
H_size2 = { # Dictionnary for syllables size 2 Hiragana
'ka':0x304B, 'ki':0x304D, 'ku':0x304F, 'ke':0x3051, 'ko':0x3053,
'ga':0x304C, 'gi':0x304E, 'gu':0x3050, 'ge':0x3052, 'go':0x3054,
'sa':0x3055,              'su':0x3059, 'se':0x305B, 'so':0x305D,
'za':0x3056, 'ji':0x3058, 'zu':0x305A, 'ze':0x305C, 'zo':0x305E,
'ta':0x305F,                           'te':0x3066, 'to':0x3068,
'da':0x3060,                           'de':0x3067, 'do':0x3069,
'na':0x306A, 'ni':0x306B, 'nu':0x306C, 'ne':0x306D, 'no':0x306E,
'ha':0x306F, 'hi':0x3072, 'fu':0x3075, 'he':0x3078, 'ho':0x307B,
'ba':0x3070, 'bi':0x3073, 'bu':0x3076, 'be':0x3079, 'bo':0x307C,
'pa':0x3071, 'pi':0x3074, 'pu':0x3077, 'pe':0x307A, 'po':0x307D,
'ma':0x307E, 'mi':0x307F, 'mu':0x3080, 'me':0x3081, 'mo':0x3082,
'ya':0x3084,              'yu':0x3086,              'yo':0x3088,
'ja':chr(0x3058)+chr(0x3083), 'ju':chr(0x3058)+chr(0x3085), 'jo':chr(0x3058)+chr(0x3087),
'ra':0x3089, 'ri':0x308A, 'ru':0x308B, 're':0x308C, 'ro':0x308D,
'wa':0x308F, 'wi':0x3090,              'we':0x3091, 'wo':0x3092
}
H_size3 = { # Dictionnary for size 3 Hiragana
'shi':0x3057, 'sha':chr(0x3057)+chr(0x3083), 'shu':chr(0x3057)+chr(0x3085), 'sho':chr(0x3057)+chr(0x3087),
'chi':0x3061, 'cha':chr(0x3061)+chr(0x3083), 'chu':chr(0x3061)+chr(0x3085), 'cho':chr(0x3061)+chr(0x3087),
'tsu':0x3064
}
H_special = { # special characters
'ltsu':0x3063, #little tsu
'ya':0x3083, 'yu':0x3085, 'yo':0x3087,
'jd':0x3062 # ji from chi
}

#main class
class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Romaji2Hiragana")
        self.geometry("800x600")
        self.iconbitmap("icon.ico") # Remove this line if you didn't download the icon file

        label1 = tk.Label(self, text="Romaji :",pady=15,font=("Times New Roman", 18))
        label1.grid(row=0,column=0)
        label2 = tk.Label(self, text="Hiragana :",pady=15,font=("Times New Roman", 18))
        label2.grid(row=0,column=1)

        self.romajiText = tk.Text(self,height=18,width=30)
        self.romajiText.configure(font=("Times New Roman", 18))
        self.romajiText.grid(row=1,column=0,padx=15)
        self.HiraganaText = tk.Text(self,height=18,width=30)
        self.HiraganaText.configure(font=("Times New Roman", 18))
        self.HiraganaText.grid(row=1,column=1,padx=15)

        self.romajiText.focus_set() # focus on romajiText
        self.bind("<Control-c>",self.copy) # when CTRL+C is clicked we call the method copy() to copy HiraganaText to clipboard

        # Call the method converse if any key is pressed, this will change the hiragana text in real time
        self.bind("<Key>",self.converse)

    def converse(self,event):
        text = self.romajiText.get(1.0,tk.END) # get all the text written in Romaji
        text=text.lower()
        H_text="" # the text that we're gonna put in Hiragana text
        i=0
        while i < len(text): # traverse the text and check if any pattern is in a dictionnary and converse it
            if i < len(text)-2 and text[i:i+3] in H_size3:
                if isinstance(H_size3[text[i:i+3]],int) :
                    H_text=H_text + chr(H_size3[text[i:i+3]])
                else:
                    H_text=H_text + H_size3[text[i:i+3]]
                i=i+3
            elif i < len(text)-1 and text[i:i+2] in H_size2:
                if isinstance(H_size2[text[i:i+2]],int) :
                    H_text=H_text + chr(H_size2[text[i:i+2]])
                else:
                    H_text=H_text + H_size2[text[i:i+2]]
                i=i+2
            elif text[i] in H_size1:
                H_text=H_text+chr(H_size1[text[i]])
                i=i+1
            elif i < len(text)-2 and text[i].isalpha() and text[i]==text[i+1]:
                H_text = H_text + chr(H_special["ltsu"])
                i=i+1
            elif i < len(text)-3 and (text[i]+'i') in H_size2 and text[i+1]=='y' and text[i+1:i+3] in H_special:
                H_text = H_text + chr(H_size2[text[i]+'i']) + chr(H_special[text[i+1:i+3]])
                i=i+3
            else: # if the text isn't proper Romaji just let the english character the same
                H_text=H_text+text[i]
                i=i+1

        self.HiraganaText.delete(1.0,tk.END)
        self.HiraganaText.insert(1.0,H_text)

    def copy(self,event):
        self.clipboard_clear()
        self.clipboard_append(self.HiraganaText.get(1.0,tk.END)) #copy everything in hiragana to clipboard
        self.update # so that the clipboard doesn't change after the program is closed


if __name__ == "__main__":
    root = Root()
    root.mainloop()
