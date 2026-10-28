# 📋 Ürün Bilgi Formu Oluşturucu (UBF Stüdyosu)

> **Kendal Elektrik A.Ş.** bünyesindeki markalar (**K2 LED Systems**, **Global Lighting**, **Vanti**) için kurumsal, standart ve hatasız A4 **Ürün Bilgi Formları** (Product Information Sheet / Datasheet) hazırlama, canlı önizleme ve tek tıkla profesyonel A4 PDF üretme platformudur.

🌐 **Canlı Web Sürümü:** [https://celikumutcan.github.io/kendal-ubf-creator/](https://celikumutcan.github.io/kendal-ubf-creator/)  
📁 **GitHub Deposu:** [https://github.com/celikumutcan/kendal-ubf-creator](https://github.com/celikumutcan/kendal-ubf-creator)

---

## 🎯 Projenin Amacı ve Kapsamı

Kendal Elektrik bünyesinde üretilen ve ithal edilen aydınlatma & elektrik ürünlerinin teknik şartnamelere, ihalelere, bayilere ve e-ticaret kanallarına yönelik **resmi Ürün Bilgi Formları (UBF)** hazırlanmaktadır.

Eski sistemde Word/Excel ortamında elle hazırlanan formlar; format kaymaları, eksik özelliklerde çirkin tire (`-`) işaretleri kalması, enerji etiketlerinin elle yanlış hesaplanması gibi problemlere yol açıyordu.

Bu stüdyo:
1. **Sıfır Hata:** Seçilmeyen özelliklerin otomatik gizlenmesi, AB standartlarında otomatik enerji sınıfı hesabı, kurumsal renk ve tipografi standartları sunar.
2. **Sıfır Bağımlılık (Zero Dependencies):** Node.js, npm, derleyici veya harici sunucu gerektirmez. Doğrudan tarayıcıda veya masaüstünde çift tıklanarak çalışır.
3. **Stajyer & Kullanıcı Dostu:** 353 ürünlük yerleşik arama kataloğu sayesinde ürün kodunu yazınca temel bilgiler ve fotoğraflar saniyeler içinde yüklenir.

---

## 🚀 Hızlı Başlangıç

### Yöntem 1: Canlı Bağlantı (Önerilen)
Doğrudan tarayıcınızdan açın:  
👉 **[https://celikumutcan.github.io/kendal-ubf-creator/](https://celikumutcan.github.io/kendal-ubf-creator/)**

### Yöntem 2: Çevrimdışı / Yerel Masaüstü
1. Klasördeki **`UBF_Baslat.bat`** dosyasına veya doğrudan **`index.html`** dosyasına çift tıklayın.
2. Google Chrome veya Microsoft Edge üzerinde stüdyo anında açılır.

---

## ✨ Temel Özellikler & Tasarım Kuralları

### 1. 🎨 Executive Dark Panel Tasarımı
- Üst gezinme çubuğu (Navbar), cam efektli (glassmorphism), koyu lacivert gradient (`#0d1527` ➔ `#080d18`) ve ışıklı rozetler ile modern bir SaaS stüdyo panelidir.
- Arama çubuğu odaklandığında mavi ışıma efekti ve kısayol rozeti (`KOD ARA`) sunar.

### 2. 🔍 Akıllı Katalog Arama (353 Ürün)
- Arama kutusuna ürün kodu (örn: `GDL414`, `KDL403`, `GES230`, `KBA742`, `KFL150`) yazıldığında:
  - Ürün adı, watt, lümen, gerilim, ebat bilgileri,
  - Ürün fotoğrafı (`images/urunler/...`),
  - Varsa teknik ölçü çizimi (`images/ubf-drawings/...`),
  - Uygun marka logosu otomatik doldurulur.

### 3. 🏷️ Kurumsal Marka Logosu Kuralı
- Formun sağ üst köşesinde sadece ürünün ait olduğu ana marka logosu yer alır:
  - **K2 LED Systems**
  - **Global Lighting**
  - **Vanti**
- **Kendal Elektrik** logosu formun en altında resmi üretici künyesi olarak yer aldığı için üst marka seçenekleri arasından kaldırılmıştır (çift logo tekrarını önleme kuralı).

### 4. ⚙️ Seçmeli & Dinamik Mekanik Özellikler
Projektörlerden spotlara kadar 10 farklı mekanik parametre sunulur:
- *Gövde, IP Koruma, IK Koruma, Ön Cam / Difüzör, Kablo Rakor, Kablo Kesiti, Boya / RAL Kodu, Montaj Tipi, Alev Yayılımı Koruması, Gövde Ebatları.*
- **Kritik Kural:** Hiçbir mekanik özellik zorunlu değildir. Seçilmeyen veya boş bırakılan özellikler formda **ASLA "-" (tire) olarak görünmez**, satır tamamen gizlenir.
- **Hızlı Şablon Butonları:**
  - 🔦 *Projektör / Dış Mekan*
  - 💡 *Panel / Spot*
  - 📏 *Bant Armatür*
  - ❌ *Hepsini Kapat*

### 5. 📐 Akıllı Koşullu Teknik Çizim Kutusu
- Eğer ürünün teknik ölçü çizimi yüklenmediyse formdaki "Teknik Çizim" başlığı ve kutusu **tamamen gizlenir**, form alanı genişletilerek boş kutu görünümü engellenir.
- Çizim yüklendiğinde otomatik olarak şık bir çerçeveyle görüntülenir.

### 6. ⚡ Otomatik AB Enerji Sınıfı Hesaplayıcı (EU 2019/2015)
- ηTM = (Işık Akısı ÷ Güç) × FTM. FTM, Giriş Gerilimi'nden otomatik seçilir: şebeke gerilimli (örn. 220-240Vac) ürünlerde **0,926**, şebeke dışı / düşük gerilimli (solar, 12V, 48V) ürünlerde **1,000**.
- Sınıflar: A ≥210 · B ≥185 · C ≥160 · D ≥135 · E ≥110 · F ≥85 · G <85 lm/W. Güç veya ışık akısı yoksa sınıf yazılmaz.

### 7. 🖨️ Kusursuz A4 PDF Çıktısı
- `@media print` ve `@page { size: A4 portrait; margin: 0; }` kuralları ile sayfa taşması yaşanmaz.
- Sağ üstteki **"PDF Olarak Kaydet (Yazdır)"** butonuna basıldığında Chrome/Edge yazdırma penceresinde kurumsal A4 PDF çıktısı alınır. İçerik tek sayfaya sığmazsa sığmayan bölümler bölünmeden 2. sayfaya geçer.

### 8. 💾 Taslak Kaydetme & Yedekleme
- Yapılan tüm düzenlemeler anlık olarak tarayıcı hafızasına (`localStorage`) kaydedilir.
- İstenirse form bir JSON dosyası olarak bilgisayara indirilebilir (`💾 Taslağı İndir`) veya önceki taslak yüklenebilir (`📂 Taslak Yükle`).

### 9. 📁 Ortak Klasör (Ekipçe Kaldığı Yerden Devam)
- Sol paneldeki **📁 Klasörü Bağla** ile şirketin ortak ağ klasörü kişi başı bir kez seçilir (Chrome/Edge). Sonraki ziyaretlerde izin, sayfaya ilk tıklamada istenir ("Her ziyarette izin ver" seçilirse bir daha sorulmaz).
- Form **otomatik kaydedilir**: her değişiklikten kısa süre sonra `<ÜRÜN KODU>.json` olarak klasöre yazılır (fotoğraf ve teknik çizim dahil). Sadece göz atılan ürünler için dosya oluşturulmaz.
- Ürün kodu aratıldığında kayıtlı UBF varsa **💾 Kayıtlı** rozeti çıkar ve form doğrudan kaldığı yerden açılır. Tüm kayıtlar **📋 Kayıtlı UBF'ler** listesinden de açılabilir.
- Otomatik kayıt başkasının kaydını asla sessizce ezmez: başkası değiştirdiyse veya form kayıtlı dosyadan açılmadıysa durur ve uyarı gösterir.
- Kullanım kılavuzu uygulama içinde **❓ Nasıl?** butonundadır.

---

## 📂 Dosya ve Dizin Yapısı

```
kendal-ubf-creator/
├── index.html           # Ana stüdyo uygulaması (HTML5, Modern CSS, Vanilla JS)
├── catalog.js           # 353 adet ürünün teknik veritabanı
├── README.md            # Kullanım kılavuzu ve proje detayları
├── AGENTS.md            # Gelecekteki AI ve geliştiriciler için kurallar & bağlam
├── UBF_Baslat.bat       # Yerel masaüstü başlatıcı
├── images/
│   ├── brands/          # K2, Global, Vanti vektörel SVG logoları
│   ├── urunler/         # Ürün fotoğrafları
│   ├── ubf-drawings/    # Ürün teknik ölçü ve çizim şemaları
│   └── kendal-logo.svg  # Alt kurumsal üretici logosu
└── scripts/
    ├── generate_sample_pdfs.py  # Headless Chrome ile toplu PDF üretim betiği
    └── docx_ubf_extractor.py    # Eski Word dokümanlarından veri çekici
```

---

## 📌 Gelecek Geliştiriciler & AI Modelleri İçin Önemli Notlar

1. **Bağımsızlık:** Bu repo `kendalwebpage` reposundan tamamen bağımsızdır. `kendalwebpage` reposunda bu projeye ait hiçbir kod veya değişiklik yapılmamalıdır.
2. **GitHub Pages Dağıtımı:** GitHub Pages doğrudan `main` dalının kök dizininden (`/`) yayınlanmaktadır. Değişiklikler `main` dalına push edildiğinde 1 dakika içinde canlıya geçer.
3. **Sıfır Bağımlılık Prensibi:** Projeye npm bağımlılığı, webpack/vite build adımı veya harici framework eklenmemelidir; tek dosya taşınabilirliği (`index.html`) korunmalıdır.

---

© 2026 **Kendal Elektrik A.Ş.** — Tüm Hakları Saklıdır.
