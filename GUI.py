import tkinter as tk
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
from matplotlib.animation import FuncAnimation

# Main Application Window
root = tk.Tk()
root.title("Advanced Polynomial Visualization Tool")
root.geometry("1000x800")
root.configure(bg="#f4f4f4")

# Variables for user input
poly_type = tk.StringVar(value="Linear Polynomial")
second_poly = tk.BooleanVar(value=False)
coefficients = {}
coefficients2 = {}

# Functions to handle polynomial and derivative plotting
def calculate_integration(coeffs, r1, r2):
    degree = len(coeffs) - 1
    coeff_list = [coeffs[k] for k in sorted(coeffs, reverse=True)]

    def poly_func(x):
        return sum(coeff_list[i] * x**(degree - i) for i in range(len(coeff_list)))

    integral, _ = quad(poly_func, r1, r2)
    return integral

def plot_polynomial():
    try:
        # Get the range and coefficients
        r1 = range_slider_1.get()
        r2 = range_slider_2.get()
        x = np.linspace(r1, r2, 500)

        poly_choice = poly_type.get()
        coeffs = {k: float(v.get()) for k, v in coefficients.items()}

        # Calculate Polynomial and Derivative
        y_poly = sum(coeffs[f"{chr(97+i)}"] * x**i for i in range(len(coeffs)))
        y_deriv = sum(i * coeffs[f"{chr(97+i)}"] * x**(i-1) for i in range(1, len(coeffs)))

        # Derivative equation formatting
        deriv_equation = " + ".join(
            f"{(i) * coeffs[f'{chr(97+i)}']}x^{i-1}"
            for i in range(1, len(coeffs))
            if coeffs[f'{chr(97+i)}'] != 0
        )
        deriv_equation = deriv_equation.replace("x^1", "x").replace("x^0", "").replace(" 1x", " x")
        if deriv_equation == "":
            deriv_equation = "0"

        # Integration
        integral = calculate_integration(coeffs, r1, r2)

        # Second Polynomial
        if second_poly.get():
            coeffs2 = {k: float(v.get()) for k, v in coefficients2.items()}
            y_poly2 = sum(coeffs2[f"{chr(97+i)}"] * x**i for i in range(len(coeffs2)))
            y_deriv2 = sum(i * coeffs2[f"{chr(97+i)}"] * x**(i-1) for i in range(1, len(coeffs2)))

        # Clear and plot
        ax.clear()
        ax.grid(True)
        ax.plot(x, y_poly, label="Polynomial 1", color="#007ACC")
        ax.plot(x, y_deriv, label="Derivative 1", linestyle="--", color="#FF5733")
        
        if second_poly.get():
            ax.plot(x, y_poly2, label="Polynomial 2", color="#28A745")
            ax.plot(x, y_deriv2, label="Derivative 2", linestyle="--", color="#FFC300")

        ax.set_xlabel("x-axis")
        ax.set_ylabel("y-axis")
        ax.legend()
        ax.set_title(f"Graph for {poly_choice}")
        results_label.config(text=f"Area Under Curve: {integral:.2f}")
        canvas_plot.draw()

    except Exception as e:
        error_label.config(text=f"Error: {str(e)}")

def animate_plot():
    try:
        # Animation for polynomial
        r1 = range_slider_1.get()
        r2 = range_slider_2.get()
        x = np.linspace(r1, r2, 500)
        coeffs = {k: float(v.get()) for k, v in coefficients.items()}
        y_poly = sum(coeffs[f"{chr(97+i)}"] * x**i for i in range(len(coeffs)))

        ax.clear()
        line_poly, = ax.plot([], [], label="Polynomial", color="#007ACC")
        ax.grid(True)

        def init():
            line_poly.set_data([], [])
            return line_poly,

        def update(frame):
            line_poly.set_data(x[:frame], y_poly[:frame])
            return line_poly,

        ani = FuncAnimation(fig, update, frames=len(x), init_func=init, blit=True, repeat=False)
        canvas_plot.draw()

    except Exception as e:
        error_label.config(text=f"Error: {str(e)}")

def reset():
    for entry in coefficients.values():
        entry.set("0")
    for entry in coefficients2.values():
        entry.set("0")
    ax.clear()
    canvas_plot.draw()
    results_label.config(text="")
    error_label.config(text="")

def save_plot():
    filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if filepath:
        fig.savefig(filepath)

# Update input fields dynamically
def update_coeff_fields(*args):
    for widget in coeff_frame.winfo_children():
        widget.destroy()
    current_poly = poly_type.get()
    coeffs_required = {
        "Linear Polynomial": ['a', 'b'],
        "Quadratic Polynomial": ['a', 'b', 'c'],
        "Cubic Polynomial": ['a', 'b', 'c', 'd'],
        "Biquadratic Polynomial": ['a', 'b', 'c', 'd', 'e'],
    }
    coefficients.clear()
    for coeff in coeffs_required[current_poly]:
        tk.Label(coeff_frame, text=f"Enter {coeff}:").pack(pady=5)
        var = tk.StringVar(value="0")
        coefficients[coeff] = var
        tk.Entry(coeff_frame, textvariable=var, width=10).pack(pady=5)

    if second_poly.get():
        tk.Label(coeff_frame, text="Second Polynomial Coefficients:").pack(pady=5)
        coefficients2.clear()
        for coeff in coeffs_required[current_poly]:
            tk.Label(coeff_frame, text=f"Enter {coeff} (Poly 2):").pack(pady=5)
            var = tk.StringVar(value="0")
            coefficients2[coeff] = var
            tk.Entry(coeff_frame, textvariable=var, width=10).pack(pady=5)

# UI Layout (HTML/CSS Inspired)
header_frame = tk.Frame(root, bg="#007ACC", padx=20, pady=10)
header_frame.pack(fill="x")

header_label = ttk.Label(header_frame, text="Polynomial Visualization Tool", font=("Arial", 18, "bold"), foreground="white", background="#007ACC")
header_label.pack()

# Canvas for scrollable area
canvas_frame = tk.Frame(root)
canvas_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(canvas_frame)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

# Scrollable window inside the canvas
scrollable_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

ttk.Label(scrollable_frame, text="Select Polynomial Type:", font=("Arial", 14)).pack(pady=10)
ttk.OptionMenu(scrollable_frame, poly_type, poly_type.get(), "Linear Polynomial", "Quadratic Polynomial", "Cubic Polynomial", "Biquadratic Polynomial").pack(pady=10)
poly_type.trace_add("write", update_coeff_fields)

coeff_frame = tk.Frame(scrollable_frame, bg="#f4f4f4")
coeff_frame.pack(pady=20)
update_coeff_fields()

range_slider_1 = tk.Scale(scrollable_frame, from_=-10, to=0, orient="horizontal", label="Lower Limit", sliderlength=20, length=400)
range_slider_1.pack(pady=10)
range_slider_2 = tk.Scale(scrollable_frame, from_=0, to=10, orient="horizontal", label="Upper Limit", sliderlength=20, length=400)
range_slider_2.pack(pady=10)

fig, ax = plt.subplots(figsize=(6, 4))
canvas_plot = FigureCanvasTkAgg(fig, master=scrollable_frame)
canvas_widget = canvas_plot.get_tk_widget()
canvas_widget.pack(pady=20)

ttk.Checkbutton(scrollable_frame, text="Enable Second Polynomial", variable=second_poly, command=update_coeff_fields).pack(pady=10)

# Create a frame for buttons to be displayed correctly
btn_frame = tk.Frame(scrollable_frame, bg="#f4f4f4")
btn_frame.pack(pady=20, fill="x")

ttk.Button(btn_frame, text="Plot Polynomial", command=plot_polynomial, width=20).grid(row=0, column=0, padx=10)
ttk.Button(btn_frame, text="Animate Plot", command=animate_plot, width=20).grid(row=0, column=1, padx=10)
ttk.Button(btn_frame, text="Reset", command=reset, width=20).grid(row=0, column=2, padx=10)
ttk.Button(btn_frame, text="Save Plot", command=save_plot, width=20).grid(row=0, column=3, padx=10)
ttk.Button(btn_frame, text="Exit", command=root.quit, width=20).grid(row=0, column=4, padx=10)

results_label = ttk.Label(scrollable_frame, text="", font=("Arial", 12))
results_label.pack(pady=10)

# Derivative equation label
deriv_label = ttk.Label(scrollable_frame, text="", font=("Arial", 12), background="#f4f4f4")
deriv_label.pack(pady=10)

error_label = ttk.Label(scrollable_frame, text="", foreground="red", background="#f4f4f4")
error_label.pack(pady=5)

# Run the Tkinter application
root.mainloop()
