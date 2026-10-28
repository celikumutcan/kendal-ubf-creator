# 🤖 AGENTS.MD — Kendal UBF Oluşturucu İçin Yapay Zeka & Geliştirici Kılavuzu

Bu belge, projede çalışacak gelecekteki yapay zeka asistanları (Antigravity, Claude, ChatGPT, Cursor vb.) ve geliştiriciler için kritik kuralları, tasarım kararlarını ve proje bağlamını özetler.

---

## 1. 📌 Proje Kimliği ve Amacı
- **Proje Adı:** Ürün Bilgi Formu Oluşturucu (Kendal UBF Creator)
- **Repo:** `celikumutcan/kendal-ubf-creator`
- **Canlı URL:** `https://celikumutcan.github.io/kendal-ubf-creator/`
- **Amaç:** Kendal Elektrik A.Ş. markaları (K2, Global, Vanti) için standart dikey A4 (gerekirse 2 sayfa) Ürün Bilgi Formu (Datasheet) oluşturmak, önizlemek ve yazdırmak/PDF almak.

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
   - Boş alanlar her zaman DOM'dan tamamen gizlenir (`display: none`). Sabit tablolarda (Optik, Elektrik) bu işi `hideEmptySpecRows()` yapar.

4. **Marka Logoları Hiyerarşisi:**
   - Üst marka logosu alanında sadece: **K2 LED Systems**, **Global Lighting**, **Vanti** bulunur.
   - **Kendal Elektrik** logosu formun en altında ("Üretici Firma: Kendal Elektrik") kalıcı olarak bulunduğu için üst marka listesinde yer almaz.

5. **A4 Baskı Uyumu:**
   - Form normalde **tek sayfa (A4 Portrait)** çıkar. İçerik sığmazsa `paginatePages()` sığmayan bölümü ve sonrasındakileri **bütün olarak** 2. sayfaya taşır (başlık + alt bilgi 2. sayfada da tekrarlanır).
   - Hiçbir bölüm (spec satırı, teknik çizim, varyant tablosu) iki sayfaya bölünmez; yeni bölüm eklerken `ubf-flow` sınıfı verilmelidir.
   - Spec blokları (Mekanik, Optik, Elektrik, Opsiyonlar, Solar) `arrangeSpecBlocks()` ile görünenler sırayla ikişer ikişer satırlara dizilir; boş blok atlanır, sıradaki yerine geçer. Yeni spec bloğu eklenirse `SPEC_BLOCK_ORDER`'a (gerekirse `SPEC_ROW_IDS`'e yeni satır) eklenmelidir.
   - Sayfa içinden taşan veya boş sayfa üreten CSS değişiklikleri engellenmelidir.

---

## 3. 📐 Mimari ve Dosya Haritası

- **`index.html`**:
  - `/* TOP NAVBAR */`: Cam efektli (glassmorphism) üst menü, canlı katalog araması ve üst butonlar.
  - `/* SIDEBAR (EDITOR) */`: Sol sütundaki veri giriş paneli (Genel bilgiler, Mekanik özellikler, Elektriksel, Optik, vb.).
  - `/* A4 PREVIEW CONTAINER */`: Sağ sütundaki canlı A4 kağıt önizleme alanı.
  - `/* PRINT STYLES */`: `@media print` kuralları ile tarayıcı yazdırma görünümü.
  - `<script>` bloğu: Form senkronizasyonu, `localStorage` oto-kayıt, EU 2019/2015 enerji etiketi hesaplama motoru, JSON import/export, dinamik mekanik özellik butonları.
  - Ortak klasör kaydı (File System Access API): UBF'ler ortak ağ klasörüne `<ÜRÜN KODU>.json` olarak yazılır/okunur; klasör izni IndexedDB'de saklanır. Form durumu `collectFormState()` / `applyFormState()` ile tek yerden toplanır — yeni bir düz alan `FORM_FIELDS`'e, mekanik/opsiyon/solar alanı ilgili `*_DEFINITIONS` dizisine eklenmelidir.
  - Enerji sınıfı (`recalculateEnergyClass`): ηTM = lm / W × FTM; FTM şebeke gerilimli üründe 0,926, şebeke dışı / düşük gerilimde 1,000 (Kalite biriminin Excel hesaplayıcısıyla aynı, Giriş Gerilimi'nden otomatik seçilir). İç ağ adresleri (IP, paylaşım yolu) bu herkese açık repoya yazılmamalıdır.

- **`catalog.js`**:
  - `window.PRODUCT_CATALOG = [...]`: 353 adet hazır ürünün kod, ad, watt, lümen, voltaj, ebat ve resim yolu verileri.

---

## 4. 💡 Yeni Bir Sohbet Başladığında Hızlı Hatırlatma
Kullanıcı yeni bir talepte bulunduğunda:
- Çalışılacak doğru dizinin `C:\Users\umutcan.celik\Documents\GitHub\kendal-ubf-creator` olduğundan emin olun.
- Yapılan değişiklikleri test edip `git -C "C:\Users\umutcan.celik\Documents\GitHub\kendal-ubf-creator" commit` ve `push origin main` ile GitHub'a gönderin.
- `kendalwebpage` çalışma alanının temiz (`git status` clean) kaldığını doğrulayın.
