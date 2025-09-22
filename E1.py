import tkinter as tk
from tkinter import messagebox, ttk
import json
import random


# ---------- Clase Pregunta ----------
class Pregunta:
    def __init__(self, enunciado, opciones, respuesta_correcta):
        self.enunciado = enunciado
        self.opciones = opciones
        self.respuesta_correcta = respuesta_correcta


# ---------- Clase QuizApp ----------
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💡 Póngase Pilas Mijo")
        self.root.geometry("850x600")
        self.root.configure(bg="#dfe6e9")

        self.tema_texto = tk.StringVar()

        # ---------- Pantalla inicial ----------
        self.frame_inicio = tk.Frame(root, bg="#74b9ff")
        self.frame_inicio.place(relx=0.5, rely=0.5, anchor="center", width=650, height=450)

        self.label_titulo = tk.Label(
            self.frame_inicio,
            text="💡 Póngase Pilas Mijo 💡",
            font=("Arial Rounded MT Bold", 28),
            bg="#74b9ff",
            fg="white"
        )
        self.label_titulo.pack(pady=40)

        self.label = tk.Label(
            self.frame_inicio,
            text="Ingresa el tema para tu Quiz:",
            font=("Arial", 14),
            bg="#74b9ff",
            fg="white"
        )
        self.label.pack(pady=10)

        self.entry = tk.Entry(
            self.frame_inicio,
            textvariable=self.tema_texto,
            width=40,
            font=("Arial", 13),
            relief="flat",
            justify="center"
        )
        self.entry.pack(pady=10, ipady=7)

        self.start_btn = tk.Button(
            self.frame_inicio,
            text="🚀 Iniciar Quiz",
            font=("Arial Rounded MT Bold", 14),
            bg="#00b894", fg="white",
            relief="flat",
            command=self.iniciar_quiz
        )
        self.start_btn.pack(pady=15, ipadx=15, ipady=8)

        self.historial_btn = tk.Button(
            self.frame_inicio,
            text="📊 Ver Historial",
            font=("Arial Rounded MT Bold", 14),
            bg="#fdcb6e", fg="#2d3436",
            relief="flat",
            command=self.ver_historial
        )
        self.historial_btn.pack(pady=10, ipadx=10, ipady=6)

        # Variables del quiz
        self.preguntas = []
        self.indice = 0
        self.respuestas_correctas = 0
        self.var_opcion = tk.IntVar()

    def generar_preguntas(self):
        return [
            Pregunta("¿Python es un lenguaje compilado o interpretado?",
                     ["Compilado", "Interpretado", "Ambos", "Ninguno"], 1),
            Pregunta("¿Cuál es la extensión de los archivos de Python?",
                     [".java", ".py", ".cpp", ".txt"], 1),
            Pregunta("¿Cuál de estos es un tipo de dato en Python?",
                     ["int", "float", "bool", "Todas"], 3),
        ]

    def iniciar_quiz(self):
        tema = self.tema_texto.get()
        if not tema:
            messagebox.showwarning("⚠️ Atención", "Por favor ingresa un tema")
            return

        self.preguntas = self.generar_preguntas()
        random.shuffle(self.preguntas)

        # Ocultar pantalla inicial
        self.frame_inicio.destroy()

        # Crear frame del quiz
        self.frame_quiz = tk.Frame(self.root, bg="#ffeaa7", bd=0)
        self.frame_quiz.place(relx=0.5, rely=0.5, anchor="center", width=700, height=450)

        self.mostrar_pregunta()

    def mostrar_pregunta(self):
        if self.indice < len(self.preguntas):
            self.var_opcion.set(-1)
            pregunta = self.preguntas[self.indice]

            self.label_pregunta = tk.Label(
                self.frame_quiz,
                text=pregunta.enunciado,
                font=("Arial Rounded MT Bold", 16),
                bg="#ffeaa7",
                fg="#2d3436",
                wraplength=600,
                justify="center"
            )
            self.label_pregunta.pack(pady=25)

            self.opciones_radio = []
            for i, op in enumerate(pregunta.opciones):
                rb = tk.Radiobutton(
                    self.frame_quiz,
                    text=op,
                    variable=self.var_opcion,
                    value=i,
                    font=("Arial", 13),
                    bg="#ffeaa7",
                    fg="#2d3436",
                    selectcolor="#fab1a0"
                )
                rb.pack(anchor="w", padx=150, pady=8)
                self.opciones_radio.append(rb)

            self.btn_siguiente = tk.Button(
                self.frame_quiz,
                text="➡ Siguiente",
                font=("Arial Rounded MT Bold", 13),
                bg="#0984e3", fg="white",
                relief="flat",
                command=self.siguiente
            )
            self.btn_siguiente.pack(pady=25, ipadx=12, ipady=6)

        else:
            self.mostrar_resultado()

    def siguiente(self):
        seleccion = self.var_opcion.get()
        if seleccion == -1:
            messagebox.showwarning("⚠️ Atención", "Debes seleccionar una opción")
            return

        if seleccion == self.preguntas[self.indice].respuesta_correcta:
            self.respuestas_correctas += 1

        # limpiar widgets
        self.label_pregunta.destroy()
        for rb in self.opciones_radio:
            rb.destroy()
        self.btn_siguiente.destroy()

        self.indice += 1
        self.mostrar_pregunta()

    def mostrar_resultado(self):
        porcentaje = (self.respuestas_correctas / len(self.preguntas)) * 100
        resultado = f"Aciertos: {self.respuestas_correctas}/{len(self.preguntas)}\nPorcentaje: {porcentaje:.2f}%"

        # Pantalla de resultados
        self.frame_quiz.destroy()
        frame_resultado = tk.Frame(self.root, bg="#55efc4", bd=0)
        frame_resultado.place(relx=0.5, rely=0.5, anchor="center", width=650, height=400)

        tk.Label(
            frame_resultado,
            text="🎉 ¡Resultados del Quiz! 🎉",
            font=("Arial Rounded MT Bold", 22),
            bg="#55efc4", fg="#2d3436"
        ).pack(pady=40)

        tk.Label(
            frame_resultado,
            text=resultado,
            font=("Arial", 16, "bold"),
            bg="#55efc4", fg="#1e272e"
        ).pack(pady=20)

        tk.Button(
            frame_resultado,
            text="Salir",
            font=("Arial Rounded MT Bold", 14),
            bg="#d63031", fg="white",
            relief="flat",
            command=self.root.quit
        ).pack(pady=30, ipadx=12, ipady=6)

        self.guardar_historial(self.respuestas_correctas, len(self.preguntas), porcentaje)

    def guardar_historial(self, aciertos, total, porcentaje):
        data = {
            "aciertos": aciertos,
            "total": total,
            "porcentaje": porcentaje
        }
        try:
            with open("historial.json", "r") as f:
                historial = json.load(f)
        except FileNotFoundError:
            historial = []
        historial.append(data)
        with open("historial.json", "w") as f:
            json.dump(historial, f, indent=4)

    def ver_historial(self):
        try:
            with open("historial.json", "r") as f:
                historial = json.load(f)
        except FileNotFoundError:
            messagebox.showinfo("📊 Historial", "Aún no hay resultados guardados")
            return

        ventana_historial = tk.Toplevel(self.root)
        ventana_historial.title("📊 Historial de Resultados")
        ventana_historial.geometry("600x400")
        ventana_historial.configure(bg="#f1f2f6")

        tk.Label(
            ventana_historial,
            text="Historial de Intentos",
            font=("Arial Rounded MT Bold", 18),
            bg="#f1f2f6", fg="#2d3436"
        ).pack(pady=15)

        tabla = ttk.Treeview(ventana_historial, columns=("intento", "aciertos", "total", "porcentaje"), show="headings")
        tabla.heading("intento", text="Intento")
        tabla.heading("aciertos", text="Aciertos")
        tabla.heading("total", text="Total")
        tabla.heading("porcentaje", text="Porcentaje")

        tabla.column("intento", width=80, anchor="center")
        tabla.column("aciertos", width=100, anchor="center")
        tabla.column("total", width=100, anchor="center")
        tabla.column("porcentaje", width=120, anchor="center")

        for i, intento in enumerate(historial, start=1):
            tabla.insert("", "end", values=(i, intento["aciertos"], intento["total"], f"{intento['porcentaje']:.2f}%"))

        tabla.pack(expand=True, fill="both", padx=20, pady=10)


# ---------- MAIN ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
