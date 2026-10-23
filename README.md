# Kendal UBF Stüdyosu (Ürün Bilgi Formu Oluşturucu)

Kendal Elektrik A.Ş. bünyesindeki markaların (K2 LED Systems, Global Lighting, Vanti) standart A4 Ürün Bilgi Formlarını (Product Information Sheet) profesyonel ve hatasız bir şekilde hazırlamak, önizlemek ve tek tıkla A4 PDF olarak dışa aktarmak için geliştirilmiş bağımsız stüdyodur.

## 🚀 Hızlı Başlangıç

Bu proje hiçbir kurulum, Node.js veya internet sunucusu **gerektirmez**.

1. Klasördeki **`UBF_Baslat.bat`** dosyasına veya doğrudan **`index.html`** dosyasına çift tıklayın.
2. Form tarayıcınızda (Google Chrome / Microsoft Edge önerilir) anında açılacaktır.

---

## 🛠️ Temel Özellikler

- **Canlı A4 Önizleme**: Sol panelde yapılan tüm değişiklikler (başlıklar, teknik özellikler, varyantlar, fotoğraflar) sağdaki A4 sayfasında anında güncellenir.
- **Dinamik Mekanik Özellikler (Seçmeli)**:
  - 10 farklı mekanik özellik (Gövde, IP, IK, Ön Cam, Kablo Rakor, Kablo, RAL Kodu, Montaj Tipi, Alev Koruması, Gövde Boyu).
  - Seçilmeyen veya boş bırakılan özellikler formda **ASLA "-" olarak yazılmaz**, tamamen gizlenir.
  - Hızlı şablon butonları: **⚡ Projektör / Dış Mekan**, **💡 Panel / Spot**, **📦 Bant Armatür**, **❌ Hepsini Kapat**.
- **Koşullu Teknik Çizim Bölümü**:
  - Ürünün teknik çizimi yüklenmediyse formda teknik çizim başlığı ve kutusu tamamen gizlenir. Sadece çizim yüklendiğinde görünür.
- **Otomatik Enerji Sınıfı Hesaplayıcı (EU 2019/2015)**:
  - Girilen Watt ve Lümen değerlerine göre etkinlik faktörünü (lm/W) ve AB enerji sınıfını (A-G) otomatik hesaplar.
- **353 Ürünlük Hazır Katalog**:
  - Arama çubuğuna model kodu (örn: `GDL414`, `KBA742`, `KFL150`) yazılarak ürün bilgileri tek tıkla forma çekilebilir.
- **Taslak Kaydetme / Dışa Aktarma**:
  - Otomatik tarayıcı hafızasına (Local Storage) kaydeder.
  - İstenirse JSON taslak dosyası olarak bilgisayara indirilebilir veya yüklenebilir.
- **🖨️ Profesyonel PDF Çıktısı**:
  - Sağ üstteki "PDF İndir / Yazdır" butonuna basılarak arka plan grafikleriyle birlikte tam 1 sayfa dikey A4 PDF alınır.

---

## 📂 Klasör Yapısı

```
kendal-ubf-creator/
├── index.html           # Ana stüdyo uygulaması (HTML5 + CSS + JavaScript)
├── catalog.js           # 353 adet hazır ürün veritabanı
├── UBF_Baslat.bat       # Tek tıkla başlatıcı
├── images/
│   ├── brands/          # K2, Global, Vanti vektörel SVG logoları
│   ├── urunler/         # Ürün fotoğrafları
│   ├── ubf-drawings/    # Teknik ölçü ve çizim şemaları
│   └── kendal-logo.svg  # Alt üretici firma logosu
└── scripts/
    ├── generate_sample_pdfs.py  # Python Chrome Headless ile toplu PDF üretici
    └── docx_ubf_extractor.py    # Eski Word formlarından otomatik veri çekici
```

---

© Kendal Elektrik A.Ş. — Tüm Hakları Saklıdır.
