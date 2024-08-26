import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, Frame, Label, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime
from PIL import Image, ImageTk

# CSV dosyasını yükleyin ve tarih sütununu datetime olarak ayarlayın
data = pd.read_csv('tcmb_aylik_veriler.csv', parse_dates=['Tarih'], index_col='Tarih')

# Dil seçenekleri
languages = {
    'English': {'title': 'Data Visualization Application', 'info': 'No data available for selected date.',
                'data_point': 'Date: {date}, Value: {value}', 'update': 'Update Graph', 'display': 'Display', 'choose_color': 'Choose Color', 'graph_type': 'Graph Type', 'yearly': 'Yearly', 'save_graph': 'Save Graph', 'statistics': 'Statistics',
                'auto_update': 'Auto Update', 'fullscreen': 'Full Screen', 'windowed': 'Windowed', },
    'Türkçe': {'title': 'Veri Görselleştirme Uygulaması', 'info': 'Seçilen tarih için veri bulunamadı.',
               'data_point': 'Tarih: {date}, Değer: {value}', 'update': 'Grafiği Güncelle', 'display': 'Göster', 'choose_color': 'Renk Seç', 'graph_type': 'Grafik Türü', 'yearly': 'Yıllık', 'save_graph': 'Grafiği Kaydet', 'statistics': 'İstatistikler',
               'auto_update': 'Otomatik Güncelleme', 'fullscreen': 'Tam Ekran', 'windowed': 'Pencere Modu', }
}
current_lang = 'Türkçe'

def set_language(lang):
    global current_lang
    current_lang = lang
    root.title(languages[lang]['title'])

    # Arayüz elemanlarının metinlerini güncelle
    elements_to_update = {
        update_button: 'update',
        color_button1: 'choose_color',
        color_button2: 'choose_color',
        save_button: 'save_graph',
        statistics_button: 'statistics',
        auto_update_check: 'auto_update',
        fullscreen_button: 'fullscreen',
        windowed_button: 'windowed'
    }

    for element, text_key in elements_to_update.items():
        element.config(text=languages[lang][text_key])

    check1.config(text=f"{languages[current_lang]['display']} {option1.get()}")
    check2.config(text=f"{languages[current_lang]['display']} {option2.get()}")

    # Yıl ve ay menüsünü güncelle
    months = [languages[current_lang]['yearly']] + list(range(1, 13))
    month_var.set(months[0])
    month_menu['menu'].delete(0, 'end')
    for month in months:
        month_menu['menu'].add_command(label=month, command=tk._setit(month_var, month))
    
    month_var2.set(months[0])
    month_menu2['menu'].delete(0, 'end')
    for month in months:
        month_menu2['menu'].add_command(label=month, command=tk._setit(month_var2, month))


    # Grafik güncelle
    plot_data()

# Ana pencereyi oluştur
root = tk.Tk()
root.title(languages[current_lang]['title'])
root.geometry('1400x900')  # Uygulamanın başlangıç boyutu
root.configure(bg='#e6e6e6')

def toggle_fullscreen():
    root.attributes("-fullscreen", True)

def exit_fullscreen():
    root.attributes("-fullscreen", False)

# Sol ana çerçeve (Ana Özellikler)
main_frame = tk.Frame(root, bg='#e6e6e6')
main_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nswe')

# Sağ yardımcı çerçeve (Yardımcı Özellikler)
side_frame = tk.Frame(root, bg='#d9d9d9', width=300)
side_frame.grid(row=0, column=1, padx=20, pady=20, sticky='nswe')

# Grafik çizdirmek için figür ve aks oluştur
fig, ax = plt.subplots(figsize=(10, 5))

# Tkinter canvas'ı matplotlib grafiğine entegre et
graph_canvas = FigureCanvasTkAgg(fig, master=main_frame)
canvas_widget = graph_canvas.get_tk_widget()
canvas_widget.grid(row=0, column=0, columnspan=4, pady=(20, 50))  # Alt çerçeveyi aşağıya almak için pady ayarı yapıldı

# Varsayılan renkler
color1 = 'red'
color2 = 'blue'

# Otomatik güncelleme fonksiyonu
def auto_update():
    if auto_update_var.get():
        plot_data()
        root.after(1000, auto_update)  # 5 saniyede bir otomatik güncelleme

def plot_data():
    ax.clear()

    # İlk yıl ve ay için veri filtreleme
    if month_var.get() == languages[current_lang]['yearly']:  # Yıl bazında veri filtreleme
        filtered_data1 = data[data.index.year == year_var.get()]
    else:  # Ay bazında veri filtreleme
        filtered_data1 = data[(data.index.year == year_var.get()) & (data.index.month == int(month_var.get()))]

    # İkinci yıl ve ay için veri filtreleme
    if month_var2.get() == languages[current_lang]['yearly']:
        filtered_data2 = data[data.index.year == year_var2.get()]
    else:
        filtered_data2 = data[(data.index.year == year_var2.get()) & (data.index.month == int(month_var2.get()))]

    # Grafik türünü al
    graph_type = graph_type_var.get()

    # İlk veri serisini çiz ve efsane ekle
    if var1.get():
        plot_series(filtered_data1, option1.get(), color1, graph_type)
    # İkinci veri serisini çiz ve efsane ekle
    if var2.get():
        plot_series(filtered_data2, option2.get(), color2, graph_type)

    ax.legend()

    # X ekseni tarih formatı düzenlemeleri
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")

    # Grafik başlık ve etiketlerini güncelle
    ax.set_title(title_entry.get())
    ax.set_xlabel(xlabel_entry.get())
    ax.set_ylabel(ylabel_entry.get())

    graph_canvas.draw()

def plot_series(filtered_data, series_name, color, graph_type):
    if graph_type == 'Line':
        line, = ax.plot(filtered_data.index, filtered_data[series_name], label=series_name, color=color, linestyle='-', marker='o')
        annotate_series(line.get_xdata(), line.get_ydata())
    elif graph_type == 'Bar':
        bars = ax.bar(filtered_data.index, filtered_data[series_name], label=series_name, color=color)
        annotate_series(filtered_data.index, filtered_data[series_name])
    elif graph_type == 'Scatter':
        scatter = ax.scatter(filtered_data.index, filtered_data[series_name], label=series_name, color=color)
        annotate_series(filtered_data.index, filtered_data[series_name])

def annotate_series(x_data, y_data):
    for x, y in zip(x_data, y_data):
        ax.annotate(f'{y:.2f}', (x, y), textcoords="offset points", xytext=(0,10), ha='center')

def choose_color(var, label):
    color_code = colorchooser.askcolor(title="Choose Color")[1]
    if color_code:
        if var == 1:
            global color1
            color1 = color_code
        else:
            global color2
            color2 = color_code
        label.config(bg=color_code)

def save_graph():
    file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG files', '*.png'), ('All files', '*.*')])
    if file_path:
        fig.savefig(file_path)

def show_statistics():
    selected_series = data[option1.get()] if var1.get() else data[option2.get()]
    if not selected_series.empty:
        stats = selected_series.describe()
        stats_message = f"""
        {languages[current_lang]['statistics']}:
        Mean: {stats['mean']:.2f}
        Median: {stats['50%']:.2f}
        Std Dev: {stats['std']:.2f}
        Max: {stats['max']:.2f}
        Min: {stats['min']:.2f}
        """
        messagebox.showinfo(languages[current_lang]['statistics'], stats_message)
    else:
        messagebox.showinfo(languages[current_lang]['statistics'], languages[current_lang]['info'])

def on_click(event):
    if event.inaxes is not None and event.xdata is not None and event.ydata is not None:
        date_str = pd.to_datetime(event.xdata, unit='D').strftime('%Y-%m')
        value_str = f"{event.ydata:.2f}"
        messagebox.showinfo("Data Point", languages[current_lang]['data_point'].format(date=date_str, value=value_str))


# Ana Özellikler - Sol Çerçeve

# Year and month selection with dropdown
years = list(range(data.index.year.min(), data.index.year.max() + 1))
default_year = max(2020, years[0])
months = [languages[current_lang]['yearly']] + list(range(1, 13))  # 'Yearly' option for full year view

# Yıl ve ay seçim değişkenleri
year_var = tk.IntVar(value=default_year)
month_var = tk.StringVar(value=months[0])

# Year ve Month menüleri
year_menu = ttk.OptionMenu(main_frame, year_var, default_year, *years)
year_menu.grid(row=1, column=0, padx=20, pady=5, sticky='ew')
month_menu = ttk.OptionMenu(main_frame, month_var, months[0], *months)
month_menu.grid(row=2, column=0, padx=20, pady=5, sticky='ew')

# İkinci Yıl ve Ay seçim değişkenleri
year_var2 = tk.IntVar(value=default_year)
month_var2 = tk.StringVar(value=months[0])

# İkinci Year ve Month menüleri
year_menu2 = ttk.OptionMenu(main_frame, year_var2, default_year, *years)
year_menu2.grid(row=1, column=1, padx=20, pady=5, sticky='ew')
month_menu2 = ttk.OptionMenu(main_frame, month_var2, months[0], *months)
month_menu2.grid(row=2, column=1, padx=20, pady=5, sticky='ew')

# Data series selection
option1 = ttk.Combobox(main_frame, values=list(data.columns), state="readonly")
option1.grid(row=3, column=0, padx=20, pady=10, sticky='ew')
option2 = ttk.Combobox(main_frame, values=list(data.columns), state="readonly")
option2.grid(row=3, column=1, padx=20, pady=10, sticky='ew')

# Color selection and display
color_frame1 = Frame(main_frame, bg="#e6e6e6")
color_frame1.grid(row=4, column=0, padx=20, pady=5, sticky='ew')
color1_label = Label(color_frame1, text="      ", bg=color1, width=2)
color1_label.pack(side=tk.LEFT)
color_button1 = ttk.Button(color_frame1, text=languages[current_lang]['choose_color'], command=lambda: choose_color(1, color1_label))
color_button1.pack(side=tk.LEFT, padx=5)

color_frame2 = Frame(main_frame, bg="#e6e6e6")
color_frame2.grid(row=4, column=1, padx=20, pady=5, sticky='ew')
color2_label = Label(color_frame2, text="      ", bg=color2, width=2)
color2_label.pack(side=tk.LEFT)
color_button2 = ttk.Button(color_frame2, text=languages[current_lang]['choose_color'], command=lambda: choose_color(2, color2_label))
color_button2.pack(side=tk.LEFT, padx=5)

# Data series display options
var1 = tk.BooleanVar(value=True)
check1 = ttk.Checkbutton(main_frame, text=f"{languages[current_lang]['display']} {option1.get()}", variable=var1)
check1.grid(row=5, column=0, padx=20, pady=5, sticky='w')
var2 = tk.BooleanVar()
check2 = ttk.Checkbutton(main_frame, text=f"{languages[current_lang]['display']} {option2.get()}", variable=var2)
check2.grid(row=5, column=1, padx=20, pady=5, sticky='w')

# Graph type selection
graph_type_var = tk.StringVar(value='Line')
graph_type_menu = ttk.OptionMenu(main_frame, graph_type_var, 'Line', 'Line', 'Bar', 'Scatter')
graph_type_menu.grid(row=6, column=0, padx=20, pady=5, sticky='ew')

# Title and labels for the graph
title_entry = ttk.Entry(main_frame, width=30)
title_entry.insert(0, 'Graph Title')
title_entry.grid(row=7, column=0, columnspan=2, padx=20, pady=5, sticky='ew')

xlabel_entry = ttk.Entry(main_frame, width=30)
xlabel_entry.insert(0, 'X-axis Label')
xlabel_entry.grid(row=8, column=0, columnspan=2, padx=20, pady=5, sticky='ew')

ylabel_entry = ttk.Entry(main_frame, width=30)
ylabel_entry.insert(0, 'Y-axis Label')
ylabel_entry.grid(row=9, column=0, columnspan=2, padx=20, pady=5, sticky='ew')

# Yardımcı Özellikler - Sağ Çerçeve

# Auto-update checkbox
auto_update_var = tk.BooleanVar()
auto_update_check = ttk.Checkbutton(side_frame, text=languages[current_lang]['auto_update'], variable=auto_update_var, command=auto_update)
auto_update_check.grid(row=7, column=0, pady=10, sticky='w')

# Update button
update_button = ttk.Button(side_frame, text=languages[current_lang]['update'], command=plot_data)
update_button.grid(row=8, column=0, pady=10, sticky='ew')

# Save graph button
save_button = ttk.Button(side_frame, text=languages[current_lang]['save_graph'], command=save_graph)
save_button.grid(row=9, column=0, pady=10, sticky='ew')

# Show statistics button
statistics_button = ttk.Button(side_frame, text=languages[current_lang]['statistics'], command=show_statistics)
statistics_button.grid(row=10, column=0, pady=10, sticky='ew')

# Fullscreen and windowed buttons
fullscreen_button = ttk.Button(side_frame, text=languages[current_lang]['fullscreen'], command=toggle_fullscreen)
fullscreen_button.grid(row=11, column=0, pady=10, sticky='ew')

windowed_button = ttk.Button(side_frame, text=languages[current_lang]['windowed'], command=exit_fullscreen)
windowed_button.grid(row=12, column=0, pady=10, sticky='ew')

# Language selection
language_var = tk.StringVar(value=current_lang)
language_menu = ttk.OptionMenu(side_frame, language_var, current_lang, *languages.keys(), command=set_language)
language_menu.grid(row=13, column=0, pady=10, sticky='ew')

root.mainloop()
