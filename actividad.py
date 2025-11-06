# Comparación práctica entre búsqueda lineal y binaria
# Autor: Edgard o Dayan - Senati

import time

class BusquedaLineal:
    def buscar(self, lista, valor):
        for i in range(len(lista)):
            if lista[i] == valor:
                return i
        return -1


class BusquedaBinaria:
    def buscar(self, lista, valor):
        inicio = 0
        fin = len(lista) - 1
        while inicio <= fin:
            medio = (inicio + fin) // 2
            if lista[medio] == valor:
                return medio
            elif lista[medio] < valor:
                inicio = medio + 1
            else:
                fin = medio - 1
        return -1


# --- Programa principal ---
lista = list(range(1, 100001))  # Lista del 1 al 100,000 (ordenada)
valor = int(input("Ingresa el número que deseas buscar: "))

print("=== COMPARACIÓN ENTRE BÚSQUEDAS ===")
print(f"Número a buscar: {valor}\n")

# --- Búsqueda lineal ---
inicio = time.time()
pos_lineal = BusquedaLineal().buscar(lista, valor)
fin = time.time()
tiempo_lineal = fin - inicio
print(f"🔹 Búsqueda Lineal → Posición: {pos_lineal}, Tiempo: {tiempo_lineal:.6f} s")

# --- Búsqueda binaria ---
inicio = time.time()
pos_binaria = BusquedaBinaria().buscar(lista, valor)
fin = time.time()
tiempo_binaria = fin - inicio
print(f"🔹 Búsqueda Binaria → Posición: {pos_binaria}, Tiempo: {tiempo_binaria:.6f} s")

# --- Comparación ---
print("\n=== RESULTADO FINAL ===")
if tiempo_lineal > tiempo_binaria:
    print("✅ La búsqueda binaria fue más rápida.")
else:
    print("✅ La búsqueda lineal fue más rápida (caso poco común).")

print("\n📊 Explicación:")
print("- La búsqueda lineal revisa cada elemento, una por una.")
print("- La búsqueda binaria divide la lista por la mitad en cada paso.")
print("- En listas grandes, la binaria casi siempre es mucho más veloz.")
print("- Si la lista no está ordenada, solo la lineal puede funcionar.")
