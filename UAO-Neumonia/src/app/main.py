# script principal de la interfaz gráfica y de la integración de las funciones.

import os
import csv
import tkinter as tk
from tkinter import END, Image, StringVar, Text, Tk, ttk, font, filedialog
from PIL import ImageTk, Image, ImageGrab
from tkinter.messagebox import askokcancel, showinfo, WARNING

import tkcap

from integrator import read_dicom, read_jpg, prediction

class App:
    def __init__(self):
        """
        Initializes the main application window for the pneumonia detection tool.

        This method sets up the main window, including its title, size, and layout.
        It also initializes various widgets such as labels, text boxes, and buttons,
        and places them in the appropriate positions within the window. Additionally,
        it sets up string variables for patient ID and result, and focuses on the
        patient ID input box when the application starts.

        Attributes:
            root (Tk): The main window of the application.
            lab1 (ttk.Label): Label for "Imagen Radiográfica".
            lab2 (ttk.Label): Label for "Imagen con Heatmap".
            lab3 (ttk.Label): Label for "Resultado".
            lab4 (ttk.Label): Label for "Cédula Paciente".
            lab5 (ttk.Label): Label for the software title.
            lab6 (ttk.Label): Label for "Probabilidad".
            ID (StringVar): String variable to hold the patient ID.
            result (StringVar): String variable to hold the result.
            text1 (ttk.Entry): Entry widget for patient ID input.
            ID_content (str): Content of the patient ID entry widget.
            text_img1 (Text): Text widget for displaying the radiographic image.
            text_img2 (Text): Text widget for displaying the heatmap image.
            text2 (Text): Text widget for displaying the result.
            text3 (Text): Text widget for displaying the probability.
            button1 (ttk.Button): Button to trigger the prediction.
            button2 (ttk.Button): Button to load an image file.
            button3 (ttk.Button): Button to clear the inputs.
            button4 (ttk.Button): Button to save the result as a PDF.
            button6 (ttk.Button): Button to save the results to a CSV file.
            array (None): Placeholder for an array element.
            reportID (int): Identification number for generating the PDF report.
        """
        self.root = Tk()
        self.root.title("(MAIN)Herramienta para la detección rápida de neumonía")

        #   BOLD FONT
        fonti = font.Font(weight="bold")

        self.root.geometry("815x560")
        self.root.resizable(0, 0)

        #   LABELS
        self.lab1 = ttk.Label(self.root, text="Imagen Radiográfica", font=fonti)
        self.lab2 = ttk.Label(self.root, text="Imagen con Heatmap", font=fonti)
        self.lab3 = ttk.Label(self.root, text="Resultado:", font=fonti)
        self.lab4 = ttk.Label(self.root, text="Cédula Paciente:", font=fonti)
        self.lab5 = ttk.Label(
            self.root,
            text="SOFTWARE PARA EL APOYO AL DIAGNÓSTICO MÉDICO DE NEUMONÍA",
            font=fonti,
        )
        self.lab6 = ttk.Label(self.root, text="Probabilidad:", font=fonti)

        #   TWO STRING VARIABLES TO CONTAIN ID AND RESULT
        self.ID = StringVar()
        self.result = StringVar()

        #   TWO INPUT BOXES
        self.text1 = ttk.Entry(self.root, textvariable=self.ID, width=10)

        #   GET ID
        self.ID_content = self.text1.get()

        #   TWO IMAGE INPUT BOXES
        self.text_img1 = Text(self.root, width=31, height=15)
        self.text_img2 = Text(self.root, width=31, height=15)
        self.text2 = Text(self.root)
        self.text3 = Text(self.root)

        #   BUTTONS
        self.button1 = ttk.Button(
            self.root, text="Predecir", state="disabled", command=self.run_model
        )
        self.button2 = ttk.Button(
            self.root, text="Cargar Imagen", command=self.load_img_file
        )
        self.button3 = ttk.Button(self.root, text="Borrar", command=self.delete)
        self.button4 = ttk.Button(self.root, text="PDF", command=self.create_pdf)
        self.button6 = ttk.Button(
            self.root, text="Guardar", command=self.save_results_csv
        )

        #   WIDGETS POSITIONS
        self.lab1.place(x=110, y=65)
        self.lab2.place(x=545, y=65)
        self.lab3.place(x=500, y=350)
        self.lab4.place(x=65, y=350)
        self.lab5.place(x=122, y=25)
        self.lab6.place(x=500, y=400)
        self.button1.place(x=220, y=460)
        self.button2.place(x=70, y=460)
        self.button3.place(x=670, y=460)
        self.button4.place(x=520, y=460)
        self.button6.place(x=370, y=460)
        self.text1.place(x=200, y=350)
        self.text2.place(x=610, y=350, width=90, height=30)
        self.text3.place(x=610, y=400, width=90, height=30)
        self.text_img1.place(x=65, y=90)
        self.text_img2.place(x=500, y=90)

        #   FOCUS ON PATIENT ID
        self.text1.focus_set()

        #  se reconoce como un elemento de la clase
        self.array = None

        #   NUMERO DE IDENTIFICACIÓN PARA GENERAR PDF
        self.reportID = 0

        #   RUN LOOP
        self.root.mainloop()

    #   METHODS
    def load_img_file(self):
        """
        Prompts the user to select an image file and loads it.
        This method opens a file dialog for the user to select an image file. 
        Supported file types are DICOM (.dcm), JPEG (.jpeg, .jpg), and PNG (.png). 
        Depending on the file extension, the appropriate function is called to read the image.
        The image is then resized and displayed in the GUI.
        Raises:
            Exception: If there is an error reading a DICOM file.
        Displays:
            A message if the file format is not supported or if no file is selected.
        """
        filepath = filedialog.askopenfilename(
            initialdir="/",
            title="Select image",
            filetypes=(
                ("DICOM", "*.dcm"),
                ("JPEG", "*.jpeg"),
                ("jpg files", "*.jpg"),
                ("png files", "*.png"),
            ),
        )


            
        if filepath:

            ext = os.path.splitext(filepath)[1].lower()

            if ext == ".dcm":
                try:
                    self.array, img2show = read_dicom(filepath)
                except Exception as e:
                    return
            elif ext in (".jpg", ".jpeg", ".png",".JPG",".JPEG"):
                self.array, img2show = read_jpg(filepath)
            else:
                self.mostrarDato("Formato de archivo no soportado.")
                return

            #self.img1 = img2show.resize((250, 250), Image.ANTIALIAS)
            self.img1 = img2show.resize((250, 250), Image.LANCZOS)
            self.img1 = ImageTk.PhotoImage(self.img1)
            self.text_img1.image_create(END, image=self.img1)
            self.button1["state"] = "enabled"
        else:
            self.mostrarDato("filepath es nulo")
            return

    def create_pdf(self):
            cap = tkcap.CAP(self.root)
            ID = "Reporte" + str(self.reportID) + ".jpg"
            img = cap.capture(ID)
            img = Image.open(ID)
            img = img.convert("RGB")
            pdf_path = r"Reporte" + str(self.reportID) + ".pdf"
            img.save(pdf_path)
            self.reportID += 1
            showinfo(title="PDF", message="El PDF fue generado con éxito.")


    def guardar_jpeg(self):
        """
        Captures the current state of the main application window and saves it as a JPEG file.
        This method creates a screenshot of the main application window and saves it to a file
        named "mi_formulario.jpg". It uses the tkcap library to perform the capture and then
        displays a message to inform the user that the capture was successful.
        Returns:
        None
        """
        # Nombre de salida
        filename = "mi_formulario.jpg"
        # Creamos el objeto de captura
        cap = tkcap.CAP(self.root)
        # Capturamos la ventana principal y guardamos
        cap.capture(filename) # Esto genera "mi_formulario.jpg"
        showinfo("Captura", f"El formulario se guardó como {filename}") 

    def run_model(self):       
        """
        Runs the prediction model on the input array, updates the UI with the prediction results.

        This method performs the following steps:
        1. Calls the `prediction` function with the input array to get the label, probability, and heatmap.
        2. Converts the heatmap array to an image and resizes it to 250x250 pixels.
        3. Converts the resized image to a PhotoImage object.
        4. Updates the UI with the heatmap image, prediction label, and probability.

        Attributes:
            self.label (str): The predicted label from the model.
            self.proba (float): The probability of the prediction.
            self.heatmap (numpy.ndarray): The heatmap array from the prediction.
            self.img2 (ImageTk.PhotoImage): The PhotoImage object of the resized heatmap.
        """
        self.label, self.proba, self.heatmap = prediction(self.array) 
        self.img2 = Image.fromarray(self.heatmap)
        #self.img2 = self.img2.resize((250, 250), Image.ANTIALIAS)

        self.img2 = self.img2.resize((250, 250), Image.LANCZOS)
        self.img2 = ImageTk.PhotoImage(self.img2)
        print("OK")
        self.text_img2.image_create(END, image=self.img2)
        self.text2.insert(END, self.label)
        self.text3.insert(END, "{:.2f}".format(self.proba) + "%")

    def save_results_csv(self):
        """
        Save the results to a CSV file.

        This method appends the current results to a CSV file named 'historial.csv'.
        The results include text from `self.text1`, a label, and a probability value
        formatted as a percentage.

        The CSV file uses a hyphen ('-') as the delimiter.

        After successfully saving the data, a message box is shown to inform the user.

        Raises:
            IOError: If the file cannot be opened or written to.
        """
        with open("historial.csv", "a") as csvfile:
            w = csv.writer(csvfile, delimiter="-")
            w.writerow(
                [self.text1.get(), self.label, "{:.2f}".format(self.proba) + "%"]
            )
            showinfo(title="Guardar", message="Los datos se guardaron con éxito.")

    def create_pdf(self):
        """
        Captures the current state of the application's root window, saves it as a JPEG image,
        converts the image to a PDF, and increments the report ID.

        The method uses the tkcap library to capture the window and the PIL library to handle
        image conversion and saving.

        Raises:
            IOError: If there is an error in saving the image or PDF.

        Side Effects:
            - Saves a JPEG image file with the current report ID.
            - Saves a PDF file with the current report ID.
            - Increments the report ID.
            - Displays a message box indicating the PDF was generated successfully.
        """       
       
        # Pedir ubicación para guardar el PDF
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Guardar PDF"
        )
        
        if not file_path:
            return  # Si el usuario cancela, no hace nada

        # Capturar la ventana principal (self.root)
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Tomar captura de la ventana completa
        img = ImageGrab.grab(bbox=(x, y, x + width, y + height))

        # Guardar la imagen capturada como un PDF
        img.save(file_path, "PDF", resolution=100)

        showinfo(title="PDF", message="El PDF fue generado con éxito.")

       

    def delete(self):
        """
        Deletes the content of multiple text and image fields after user confirmation.

        Prompts the user with a confirmation dialog. If the user confirms, it deletes the content
        of text fields `text1`, `text2`, `text3` and image fields `text_img1`, `text_img2`.
        Displays an information dialog upon successful deletion.

        Returns:
            None
        """
        answer = askokcancel(
            title="Confirmación", message="Se borrarán todos los datos.", icon=WARNING
        )
        if answer:
            self.text1.delete(0, "end")
            self.text2.delete(1.0, "end")
            self.text3.delete(1.0, "end")
            self.text_img1.delete(self.img1, "end")
            self.text_img2.delete(self.img2, "end")
            showinfo(title="Borrar", message="Los datos se borraron con éxito")


    def mostrarDato(self,filepath):
        """
        Displays a message box with the provided file path.

        Args:
            filepath (str): The file path to be displayed in the message box.

        Returns:
            None
        """
        root = Tk()
        root.withdraw() 


        showinfo("Información", filepath)


        root.destroy()            


def main():
    my_app = App()
    return 0


if __name__ == "__main__":
    main()