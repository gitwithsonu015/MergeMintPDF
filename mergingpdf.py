from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter
import os

ctk.set_appearance_mode("System")  # Light, Dark, System
ctk.set_default_color_theme("green")  # You can also use green or dark-blue

class PDFToolApp(ctk.CTk,FastAPI):
    def __init__(self):
        super().__init__()
        self.title("🧩 Merge❤️Mint")
        self.geometry("1000x800")
        self.resizable(False, False)

        self.merge_files = []

        # === Title ===
        self.title_label = ctk.CTkLabel(self, text="📄 MergeMint PDF Tool", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=20)

        # === Merge Frame ===
        self.merge_frame = ctk.CTkFrame(self)
        self.merge_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(self.merge_frame, text="🔗 Merge PDFs", font=("Arial", 16)).pack(pady=5)

        self.file_listbox = ctk.CTkTextbox(self.merge_frame, height=100)
        self.file_listbox.pack(pady=5, padx=10, fill="x")

        ctk.CTkButton(self.merge_frame, text="➕ Add PDFs", command=self.add_merge_files).pack(pady=5)
        ctk.CTkButton(self.merge_frame, text="📌 Merge Now", command=self.merge_pdfs).pack(pady=5)

        # === Divider ===
        ctk.CTkLabel(self, text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", text_color="#888").pack(pady=10)

        # === Split Frame ===
        self.split_frame = ctk.CTkFrame(self)
        self.split_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(self.split_frame, text="✂️ Split PDF", font=("Arial", 16)).pack(pady=5)
        ctk.CTkButton(self.split_frame, text="📂 Select PDF & Split", command=self.split_pdf).pack(pady=5)

        # === Footer ===
        ctk.CTkLabel(self, text="Made By Sonu Using Python & CustomTkinter", font=("Arial", 12)).pack(pady=10)

    def add_merge_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for file in files:
            if file not in self.merge_files:
                self.merge_files.append(file)
                self.file_listbox.insert("end", f"{os.path.basename(file)}\n")

    def merge_pdfs(self):
        if not self.merge_files:
            messagebox.showwarning("No Files", "Please add PDFs to merge.")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", title="Save Merged PDF As")
        if not output_file:
            return

        writer = PdfWriter()
        try:
            for file in self.merge_files:
                reader = PdfReader(file)
                for page in reader.pages:
                    writer.add_page(page)

            with open(output_file, "wb") as f:
                writer.write(f)

            messagebox.showinfo("Success", f"PDFs merged successfully!\nSaved to:\n{output_file}")
            self.file_listbox.delete("1.0", "end")
            self.merge_files = []

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def split_pdf(self):
        file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not file:
            return

        output_dir = filedialog.askdirectory(title="Select Output Folder")
        if not output_dir:
            return

        try:
            reader = PdfReader(file)
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                out_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(file))[0]}_page_{i+1}.pdf")
                with open(out_path, "wb") as f:
                    writer.write(f)

            messagebox.showinfo("Success", f"PDF split into {len(reader.pages)} pages.\nSaved in: {output_dir}")

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = PDFToolApp()
    app.mainloop()
