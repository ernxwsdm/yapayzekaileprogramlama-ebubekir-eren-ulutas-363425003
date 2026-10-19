import os
from google import genai
from google.genai import errors, types


def kod_optimize_et(spagetti_kod: str) -> None:
  os.system("cls" if os.name == "nt" else "clear")

  print("=" * 75)
  print(" YAPAY ZEKA DESTEKLİ KOD İYİLEŞTİRME VE OPTİMİZASYON ".center(75))
  print("=" * 75)

  # API anahtarını tanımla
  api_anahtari = "AQ.Ab8RN6I_6Qwlj0xwDI5tHKYze1goMMMmx9yGGaQghwvAzNq07Q"

  if not api_anahtari:
    print("\n[HATA] API anahtarı tanımlanmamış!")
    return

  sistem_mesaji = """
    Sen kıdemli bir Yazılım Mimarı ve Performans Uzmanısın.

    Kullanıcının gönderdiği kötü yazılmış (spagetti)
    Python kodunu analiz et.

    1. Değişken isimlerini anlamlı hale getir (Clean Code).
    2. Algoritmanın çalışma hızını iyileştir.
        Örneğin O(n^2) yerine mümkünse O(n) kullan.
    3. Type Hint (Tip belirteçleri) ekle.
    4. Kodun mevcut işlevselliğini koru.
    5. Gereksiz döngüleri ortadan kaldır.

    Çıktın KESİNLİKLE sadece düzeltilmiş Python kodu olmalıdır.
    Ek açıklama veya Markdown yazma.
    """

  print("\n[AŞAMA 1] OPTİMİZE EDİLECEK SPAGETTİ KOD SİSTEME ALINDI...")
  print("[AŞAMA 2] REFACTORING İÇİN YAPAY ZEKAYA BAĞLANILIYOR...\n")

  try:
    # Yeni google-genai SDK istemcisini başlat
    client = genai.Client(api_key=api_anahtari)

    # Gemini modelini güncel sürümle (gemini-3.8-flash) çağırıyoruz
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=spagetti_kod,
        config=types.GenerateContentConfig(
            system_instruction=sistem_mesaji,
            temperature=0.2,
        ),
    )

    print("[AŞAMA 3] KOD BAŞARIYLA İYİLEŞTİRİLDİ!\n")
    print("=" * 75)
    print(" OPTİMİZE EDİLMİŞ KOD ".center(75))
    print("=" * 75)
    print(response.text)
    print("=" * 75)

  except errors.APIError as e:
    print(f"\n[API HATASI] Gemini ile iletişim kurulamadı: {e}")
  except Exception as e:
    print(f"\n[HATA] Beklenmeyen bir hata oluştu: {e}")


# Örnek Test Kullanımı
if __name__ == "__main__":
  ornek_spagetti = """
def hsp(lst):
    t = 0
    for i in range(len(lst)):
        for j in range(len(lst)):
            if i == j:
                t = t + lst[i]
    return t
    """

  kod_optimize_et(ornek_spagetti)