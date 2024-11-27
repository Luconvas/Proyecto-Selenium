import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import tkinter as tk
from tkinter import filedialog, simpledialog
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

def configurar_navegador():
    firefox_options = Options()
    firefox_options.set_preference("general.useragent.override", 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

    carpeta_descargas = os.path.join(os.path.expanduser('~'), 'Downloads/Certificados')
    os.makedirs(carpeta_descargas, exist_ok=True)
    firefox_options.set_preference("browser.download.folderList", 2)
    firefox_options.set_preference("browser.download.manager.showWhenStarting", False)
    firefox_options.set_preference("browser.download.dir", carpeta_descargas)
    firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    firefox_options.set_preference("pdfjs.disabled", True)
    firefox_options.add_argument("--kiosk-printing")

    return webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    archivo = filedialog.askopenfilename(title="Selecciona el archivo Excel con los RUTs")
    root.destroy()
    return archivo

def solicitar_credenciales():
    root = tk.Tk()
    root.withdraw()

    usuario = simpledialog.askstring("Usuario", "Introduce tu usuario:", parent=root)
    contraseña = simpledialog.askstring("Contraseña", "Introduce tu contraseña:", parent=root, show='*')

    root.destroy()
    return usuario, contraseña

def iniciar_sesion(driver, usuario, contraseña):
    driver.get("https://rndpa.srcei.cl/rndpa/#/sesion/search")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Usuario")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))

    campo_usuario = driver.find_element(By.ID, "Usuario")
    campo_usuario.send_keys(usuario)

    campo_contraseña = driver.find_element(By.ID, "password")
    campo_contraseña.send_keys(contraseña)
    campo_contraseña.send_keys(Keys.RETURN)
    time.sleep(10)

def procesar_ruts(archivo_excel, driver):
    df = pd.read_excel(archivo_excel)
    ruts = df['RUT']
    data = []

    for rut in ruts:
        driver.get("https://rndpa.srcei.cl/rndpa/#/sesion/search")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "runDeudorBuscador")))

        input_field = driver.find_element(By.ID, "runDeudorBuscador")
        input_field.clear()
        input_field.send_keys(rut)
        input_field.send_keys(Keys.RETURN)
        time.sleep(2)
        
        try:
            rut_info = driver.find_element(By.XPATH, '//*[@id="main"]/div/app-admin-search-deudor/section/div/form/div/div/div[3]/rndpa-table/div/table/tbody/tr/td[1]/div/div').text
            nombre_completo = driver.find_element(By.XPATH, '//*[@id="main"]/div/app-admin-search-deudor/section/div/form/div/div/div[3]/rndpa-table/div/table/tbody/tr/td[2]/div/div').text
            estado = driver.find_element(By.XPATH, '//*[@id="main"]/div/app-admin-search-deudor/section/div/form/div/div/div[3]/rndpa-table/div/table/tbody/tr/td[3]/div/div/span').text

            data.append([rut, rut_info, nombre_completo, estado])

        except Exception as e:
            print(f"No se pudo procesar la información para el RUT {rut}. Error: {e}")
            
    output_excel_path = os.path.splitext(archivo_excel)[0] + "_resultados.xlsx"
    df_resultado = pd.DataFrame(data, columns=['RUT', 'Rut Info', 'Nombre Completo', 'Estado'])
    df_resultado.to_excel(output_excel_path, index=False)

    driver.quit()

if __name__ == "__main__":
    start_time = time.time()  # Inicio del registro de tiempo

    archivo_excel = seleccionar_archivo()
    if archivo_excel:
        usuario, contraseña = solicitar_credenciales()
        if usuario and contraseña:
            driver = configurar_navegador()
            iniciar_sesion(driver, usuario, contraseña)
            procesar_ruts(archivo_excel, driver)
        else:
            print("No se proporcionaron credenciales.")
    else:
        print("No se seleccionó ningún archivo.")
    
    end_time = time.time()  # Fin del registro de tiempo
    total_time = end_time - start_time
    print(f"El proceso completo tomó {total_time} segundos.")
