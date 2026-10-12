import json
import os
from google import genai
from google.genai import types

# API anahtarınızı buraya ekleyin veya çevre değişkeni olarak tanımlayın
client = genai.Client(api_key="AQ.Ab8RN6IECY6sXP0stcPlpDhsGgQfzfB7Guvkb9NXGQq3ySf0qw")
DOSYA_ADI = "urunler.json"


def e_ticaret_api_simulasyonu(urun_aciklamasi):
  """Gemini API kullanarak ürün detaylarını analiz eder ve JSON sözlük olarak döndürür."""
  prompt = f"""
    Aşağıdaki ürün açıklamasını analiz et ve JSON formatında şu alanları döndür:
    - urun_adi (string)
    - kategori (string)
    - seo_etiketleri (string, virgülle ayrılmış 3 adet)
    - satis_aciklamasi (string, tam 2 cümlelik satış açıklaması)

    Ürün Açıklaması: {urun_aciklamasi}
    """

  try:
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        ),
    )
    return json.loads(response.text)
  except Exception as e:
    print(f"[HATA] API çağrısı sırasında bir hata oluştu: {e}")
    return None


def verileri_yukle():
  """urunler.json dosyasından mevcut ürünleri yükler."""
  if not os.path.exists(DOSYA_ADI):
    return []
  try:
    with open(DOSYA_ADI, "r", encoding="utf-8") as f:
      icerik = f.read().strip()
      if not icerik:
        return []
      return json.loads(icerik)
  except (json.JSONDecodeError, Exception):
    print(
        "[UYARI] Bozuk veya geçersiz JSON dosyası algılandı. Liste sıfırdan"
        " başlatılıyor."
    )
    return []


def verileri_kaydet(urunler):
  """Ürün listesini urunler.json dosyasına kaydeder."""
  try:
    with open(DOSYA_ADI, "w", encoding="utf-8") as f:
      json.dump(urunler, f, ensure_ascii=False, indent=4)
  except Exception as e:
    print(f"[HATA] Dosya kaydetme sırasında hata oluştu: {e}")


def yeni_urun_ekle(urunler):
  """Kullanıcıdan veri alarak yeni ürün ekler ve Gemini ile analiz eder."""
  print("\n--- Yeni Ürün Ekle ---")
  urun_aciklamasi = input("Ürün açıklaması: ").strip()
  if not urun_aciklamasi:
    print("[HATA] Ürün açıklaması boş olamaz.")
    return

  try:
    fiyat = float(input("Ürün fiyatı: "))
    if fiyat < 0:
      print("[HATA] Fiyat negatif olamaz.")
      return
  except ValueError:
    print("[HATA] Geçersiz fiyat girdisi. Sayı girilmelidir.")
    return

  try:
    stok = int(input("Stok miktarı: "))
    if stok < 0:
      print("[HATA] Stok miktarı negatif olamaz.")
      return
  except ValueError:
    print("[HATA] Geçersiz stok girdisi. Tam sayı girilmelidir.")
    return

  print("[API] Ürün bilgileri oluşturuluyor...")
  analiz = e_ticaret_api_simulasyonu(urun_aciklamasi)

  if not analiz:
    print("[HATA] Ürün analiz edilemedi, kayıt yapılamadı.")
    return

  # Benzersiz ürün kodu oluşturma (URN-0001, URN-0002...)
  yeni_id = len(urunler) + 1
  urun_kodu = f"URN-{yeni_id:04d}"

  yeni_urun = {
      "urun_kodu": urun_kodu,
      "urun_adi": analiz.get("urun_adi", "Bilinmiyor"),
      "kategori": analiz.get("kategori", "Bilinmiyor"),
      "seo_etiketleri": analiz.get("seo_etiketleri", ""),
      "satis_aciklamasi": analiz.get("satis_aciklamasi", ""),
      "fiyat": fiyat,
      "stok": stok,
  }

  urunler.append(yeni_urun)
  verileri_kaydet(urunler)

  print("[BAŞARILI] Ürün kaydedildi.")
  print(f"Ürün Kodu      : {yeni_urun['urun_kodu']}")
  print(f"Ürün Adı       : {yeni_urun['urun_adi']}")
  print(f"Kategori       : {yeni_urun['kategori']}")
  print(f"Fiyat          : {yeni_urun['fiyat']} TL")
  print(f"Stok           : {yeni_urun['stok']}")
  print(f"SEO            : {yeni_urun['seo_etiketleri']}")

  if stok == 0:
    print("[UYARI] STOKTA YOK!")
  elif 1 <= stok <= 4:
    print(f"[UYARI] KRİTİK STOK! Yalnızca {stok} adet kaldı.")


def urunleri_listele(urunler):
  """Kayıtlı tüm ürünleri listeleyen fonksiyon."""
  print("\n--- Ürünleri Listele ---")
  if not urunler:
    print("[UYARI] Listede henüz hiç ürün bulunmamaktadır.")
    return

  for u in urunler:
    print(
        f"Kod: {u['urun_kodu']} | Ad: {u['urun_adi']} | Kategori:"
        f" {u['kategori']} | Fiyat: {u['fiyat']} TL | Stok: {u['stok']}"
    )


def urun_ara(urunler):
  """Ürün adı veya kodu ile kısmi ve büyük/küçük harf duyarsız arama yapar."""
  print("\n--- Ürün Ara ---")
  if not urunler:
    print("[UYARI] Aranacak kayıt bulunmuyor.")
    return

  aranan = input("Aranacak ürün (ad veya kod): ").strip().lower()
  bulunanlar = [
      u
      for u in urunler
      if aranan in u["urun_kodu"].lower() or aranan in u["urun_adi"].lower()
  ]

  if bulunanlar:
    print(f"[SONUÇ] {len(bulunanlar)} ürün bulundu:")
    for u in bulunanlar:
      print(f" - {u['urun_kodu']} | {u['urun_adi']} (Stok: {u['stok']})")
  else:
    print("[BİLGİ] Eşleşen ürün bulunamadı.")


def stok_guncelle(urunler):
  """Ürün kodu ile stok miktarını günceller."""
  print("\n--- Stok Güncelle ---")
  if not urunler:
    print("[UYARI] Güncellenecek ürün bulunmuyor.")
    return

  kod = input("Ürün kodu: ").strip().upper()
  urun = next((u for u in urunler if u["urun_kodu"] == kod), None)

  if not urun:
    print("[HATA] Bu koda sahip ürün bulunamadı.")
    return

  try:
    eski_stok = urun["stok"]
    yeni_stok = int(input("Yeni stok miktarı: "))
    if yeni_stok < 0:
      print("[HATA] Stok negatif olamaz.")
      return
    urun["stok"] = yeni_stok
    verileri_kaydet(urunler)
    print(f"[BAŞARILI] Stok {eski_stok}->{yeni_stok} olarak güncellendi.")
  except ValueError:
    print("[HATA] Geçersiz stok değeri girdiniz.")


def ana_menu():
  """Uygulama menüsünü çalıştıran ana döngü."""
  urunler = verileri_yukle()

  while True:
    print("\n== E-TICARET YÖNETİM PANELI ==")
    print("1 Yeni Ürün Ekle")
    print("2 Ürünleri Listele")
    print("3 Ürün Ara")
    print("4 Stok Güncelle")
    print("5 - Çıkış")

    secim = input("Seçiminiz: ").strip()

    if secim == "1":
      yeni_urun_ekle(urunler)
    elif secim == "2":
      urunleri_listele(urunler)
    elif secim == "3":
      urun_ara(urunler)
    elif secim == "4":
      stok_guncelle(urunler)
    elif secim == "5":
      print("Programdan çıkılıyor. İyi günler!")
      break
    else:
      print("[HATA] Geçersiz seçim! Lütfen 1-5 arasında bir değer girin.")


if __name__ == "__main__":
  ana_menu()