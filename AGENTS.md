# 🤖 AGENTS.MD — Kendal UBF Oluşturucu İçin Yapay Zeka & Geliştirici Kılavuzu

Bu belge, projede çalışacak gelecekteki yapay zeka asistanları (Antigravity, Claude, ChatGPT, Cursor vb.) ve geliştiriciler için kritik kuralları, tasarım kararlarını ve proje bağlamını özetler.

---

## 1. 📌 Proje Kimliği ve Amacı
- **Proje Adı:** Ürün Bilgi Formu Oluşturucu (Kendal UBF Creator)
- **Repo:** `celikumutcan/kendal-ubf-creator`
- **Canlı URL:** `https://celikumutcan.github.io/kendal-ubf-creator/`
- **Amaç:** Kendal Elektrik A.Ş. markaları (K2, Global, Vanti) için standart 1 sayfalık dikey A4 Ürün Bilgi Formu (Datasheet) oluşturmak, önizlemek ve yazdırmak/PDF almak.

---

## 2. ⚠️ ASLA ÇİĞNENMEMESİ GEREKEN KURALLAR (CRITICAL CONSTRAINTS)

1. **`kendalwebpage` Reposuna Dokunulmayacak:**
   - Bu proje `kendal-ubf-creator` reposunda bağımsız olarak yaşar.
   - Kullanıcının `kendalwebpage` ana web sitesi reposunda herhangi bir değişiklik YAPILMAMALIDIR.

2. **Sıfır Derleme / Sıfır Bağımlılık (No Build Step):**
   - Proje saf HTML5, Vanilla CSS3 ve Vanilla JavaScript (`catalog.js`) mimarisine sahiptir.
   - `package.json`, `npm install`, `vite`, `next` veya harici derleme araçları eklenmemelidir. Kullanıcı çift tıklayarak yerel olarak veya GitHub Pages üzerinden doğrudan çalıştırabilmelidir.

3. **Tire (`-`) Karakteri Kuralı:**
   - Boş bırakılan veya seçilmeyen hiçbir teknik/mekanik özellik forma `-` (tire) olarak yazdırılmaz.
   - Boş alanlar her zaman DOM'dan tamamen gizlenir (`display: none`).

4. **Marka Logoları Hiyerarşisi:**
   - Üst marka logosu alanında sadece: **K2 LED Systems**, **Global Lighting**, **Vanti** bulunur.
   - **Kendal Elektrik** logosu formun en altında ("Üretici Firma: Kendal Elektrik") kalıcı olarak bulunduğu için üst marka listesinde yer almaz.

5. **A4 Baskı Uyumu:**
   - Form çıktısı kesinlikle **tek sayfa (1 Page A4 Portrait)** kalmalıdır. Sayfa altına taşan veya ikinci boş sayfa üreten CSS değişiklikleri kesinlikle engellenmelidir.

---

## 3. 📐 Mimari ve Dosya Haritası

- **`index.html`**:
  - `/* TOP NAVBAR */`: Cam efektli (glassmorphism) üst menü, canlı katalog araması ve üst butonlar.
  - `/* SIDEBAR (EDITOR) */`: Sol sütundaki veri giriş paneli (Genel bilgiler, Mekanik özellikler, Elektriksel, Optik, vb.).
  - `/* A4 PREVIEW CONTAINER */`: Sağ sütundaki canlı A4 kağıt önizleme alanı.
  - `/* PRINT STYLES */`: `@media print` kuralları ile tarayıcı yazdırma görünümü.
  - `<script>` bloğu: Form senkronizasyonu, `localStorage` oto-kayıt, EU 2019/2015 enerji etiketi hesaplama motoru, JSON import/export, dinamik mekanik özellik butonları.

- **`catalog.js`**:
  - `window.PRODUCT_CATALOG = [...]`: 353 adet hazır ürünün kod, ad, watt, lümen, voltaj, ebat ve resim yolu verileri.

---

## 4. 💡 Yeni Bir Sohbet Başladığında Hızlı Hatırlatma
Kullanıcı yeni bir talepte bulunduğunda:
- Çalışılacak doğru dizinin `C:\Users\umutcan.celik\Documents\GitHub\kendal-ubf-creator` olduğundan emin olun.
- Yapılan değişiklikleri test edip `git -C "C:\Users\umutcan.celik\Documents\GitHub\kendal-ubf-creator" commit` ve `push origin main` ile GitHub'a gönderin.
- `kendalwebpage` çalışma alanının temiz (`git status` clean) kaldığını doğrulayın.
