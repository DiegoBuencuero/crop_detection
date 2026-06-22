"""
Script para ANALIZAR y ajustar rangos HSV de cultivos
Uso: python ml_modules/analisis_hsv.py <ruta_imagen>
"""

import cv2
import numpy as np
import sys


def analizar_imagen(ruta_imagen):
    """Carga imagen y muestra estadísticas HSV"""

    print(f"\n📷 Analizando: {ruta_imagen}\n")

    # 1. Cargar imagen
    img = cv2.imread(ruta_imagen)
    if img is None:
        print("❌ Error: No se pudo cargar la imagen")
        return

    print(f"✓ Imagen cargada: {img.shape[0]}x{img.shape[1]} píxeles")

    # 2. Convertir RGB → HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 3. Mostrar estadísticas HSV
    print("\n" + "="*50)
    print("📊 ESTADÍSTICAS HSV")
    print("="*50)

    # Separar canales
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]

    print(f"\n🎨 HUE (Color):")
    print(f"   Min: {h.min()}")
    print(f"   Max: {h.max()}")
    print(f"   Promedio: {h.mean():.1f}")
    print(f"   Desv. Est: {h.std():.1f}")

    print(f"\n🔆 SATURATION (Intensidad):")
    print(f"   Min: {s.min()}")
    print(f"   Max: {s.max()}")
    print(f"   Promedio: {s.mean():.1f}")

    print(f"\n💡 VALUE (Brillo):")
    print(f"   Min: {v.min()}")
    print(f"   Max: {v.max()}")
    print(f"   Promedio: {v.mean():.1f}")

    # 4. Mostrar percentiles (útil para rangos)
    print("\n" + "="*50)
    print("📈 PERCENTILES (para ajustar rangos)")
    print("="*50)

    h_sorted = np.sort(h.flatten())
    s_sorted = np.sort(s.flatten())
    v_sorted = np.sort(v.flatten())

    print(f"\n🎨 HUE:")
    print(f"   10%: {np.percentile(h_sorted, 10):.0f}")
    print(f"   25%: {np.percentile(h_sorted, 25):.0f}")
    print(f"   50%: {np.percentile(h_sorted, 50):.0f}")
    print(f"   75%: {np.percentile(h_sorted, 75):.0f}")
    print(f"   90%: {np.percentile(h_sorted, 90):.0f}")

    print(f"\n🔆 SATURATION:")
    print(f"   10%: {np.percentile(s_sorted, 10):.0f}")
    print(f"   25%: {np.percentile(s_sorted, 25):.0f}")
    print(f"   50%: {np.percentile(s_sorted, 50):.0f}")
    print(f"   75%: {np.percentile(s_sorted, 75):.0f}")
    print(f"   90%: {np.percentile(s_sorted, 90):.0f}")

    print(f"\n💡 VALUE:")
    print(f"   10%: {np.percentile(v_sorted, 10):.0f}")
    print(f"   25%: {np.percentile(v_sorted, 25):.0f}")
    print(f"   50%: {np.percentile(v_sorted, 50):.0f}")
    print(f"   75%: {np.percentile(v_sorted, 75):.0f}")
    print(f"   90%: {np.percentile(v_sorted, 90):.0f}")

    # 5. Sugerir rango
    print("\n" + "="*50)
    print("💡 RANGO SUGERIDO para este cultivo:")
    print("="*50)

    h_min = max(0, int(np.percentile(h_sorted, 10)))
    h_max = min(180, int(np.percentile(h_sorted, 90)))
    s_min = max(0, int(np.percentile(s_sorted, 10)))
    s_max = 255
    v_min = max(0, int(np.percentile(v_sorted, 10)))
    v_max = 255

    print(f"\nlower = ({h_min}, {s_min}, {v_min})")
    print(f"upper = ({h_max}, {s_max}, {v_max})")

    print("\n✓ Copia estos rangos a processors.py en cultivos_colores\n")

    # 6. Mostrar máscara con el rango sugerido
    print("📋 Probando máscara con rango sugerido...")
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(hsv, lower, upper)

    pixeles_detectados = cv2.countNonZero(mask)
    porcentaje = (pixeles_detectados / mask.size) * 100

    print(f"   Píxeles detectados: {pixeles_detectados}")
    print(f"   Porcentaje: {porcentaje:.2f}%")

    if porcentaje < 5:
        print("   ⚠️  MUY BAJO - Ajusta los rangos")
    elif porcentaje > 50:
        print("   ⚠️  MUY ALTO - El rango es muy amplio")
    else:
        print("   ✓ Rango parece OK")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("❌ Uso: python ml_modules/analisis_hsv.py <ruta_imagen>")
        print("   Ejemplo: python ml_modules/analisis_hsv.py media/uploads/2024/06/21/trigo.jpg")
        sys.exit(1)

    ruta = sys.argv[1]
    analizar_imagen(ruta)
