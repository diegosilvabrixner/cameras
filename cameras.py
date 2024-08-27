import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence

current_animation = None
frames_cache = {}

def open_camera(camera_n, label):
    global current_animation

    image_locais = {
        1: "C:/Users/diego/diretorio_gifs/camera1.gif",
        2: "C:/Users/diego/diretorio_gifs/camera2.gif",
        3: "C:/Users/diego/diretorio_gifs/camera3.gif",
    }
    
    image_local = image_locais.get(camera_n)
    
    if image_local:
        try:
            img = Image.open(image_local)

            standard_size = (385, 580)
            frames = [ImageTk.PhotoImage(frame.resize(standard_size, Image.Resampling.LANCZOS)) for frame in ImageSequence.Iterator(img)]

            frames_cache[camera_n] = frames

            if current_animation:
                label.after_cancel(current_animation)
                current_animation = None

            animate(label, frames)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar o GIF: {str(e)}")
    else:
        messagebox.showerror("Erro", "Câmera não encontrada.")

def animate(label, frames, delay=100, frame_idx=0):
    global current_animation

    frame = frames[frame_idx]
    label.config(image=frame)
    label.image = frame  
    next_frame_idx = (frame_idx + 1) % len(frames)

    current_animation = label.after(delay, animate, label, frames, delay, next_frame_idx)

def on_enter(event):
    event.widget['background'] = '#555555'

def on_leave(event):
    event.widget['background'] = '#333333'

def main():
    root = tk.Tk()
    root.title("Visualizador de Câmeras de Segurança")
    root.configure(bg='black')
    
    image_label = tk.Label(root, bg='black')
    image_label.pack(pady=20)
    
    button_frame = tk.Frame(root, bg='black')
    button_frame.pack()
    
    for i in range(1, 4):
        btn = tk.Button(button_frame, text=f"Câmera {i}", font=('Arial', 18), bg='#333333', fg='white', 
                        activebackground='#555555', borderwidth=0, relief='solid')
        btn.configure(command=lambda i=i: open_camera(i, image_label))
        btn.grid(row=0, column=i-1, padx=10)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.configure(width=10, height=2)

    close_button = tk.Button(root, text="Fechar", font=('Arial', 16), bg='#333333', fg='white', 
                             activebackground='#555555', borderwidth=0, relief='solid', 
                             command=root.quit)
    close_button.pack(pady=20)
    close_button.bind("<Enter>", on_enter)
    close_button.bind("<Leave>", on_leave)

    root.mainloop()

if __name__ == "__main__":
    main()
