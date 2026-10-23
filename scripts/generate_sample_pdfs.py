import os
import re
import base64
import subprocess

WORKSPACE = r"c:\Users\umutcan.celik\Documents\GitHub\kendalwebpage"
OUT_DIR = r"C:\Users\umutcan.celik\Desktop\UBF-Ornek-PDFler"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

os.makedirs(OUT_DIR, exist_ok=True)

def load_prefixed_svg(relpath, prefix):
    filepath = os.path.join(WORKSPACE, relpath)
    if not os.path.exists(filepath):
        return ""
    with open(filepath, "r", encoding="utf-8") as f:
        c = f.read()
    c = re.sub(r'\bst(\d+)\b', f'{prefix}\\1', c)
    c = c.replace('#clippath', f'#{prefix}_clip')
    c = c.replace('id="clippath"', f'id="{prefix}_clip"')
    c = c.replace("id='clippath'", f"id='{prefix}_clip'")
    return c

def to_base64_data_uri(filepath):
    if not os.path.exists(filepath):
        return ""
    with open(filepath, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
        if filepath.endswith(".svg"):
            mime = "image/svg+xml"
        elif filepath.endswith(".webp"):
            mime = "image/webp"
        elif filepath.endswith(".jpeg") or filepath.endswith(".jpg"):
            mime = "image/jpeg"
        elif filepath.endswith(".png"):
            mime = "image/png"
        else:
            mime = "application/octet-stream"
        return f"data:{mime};base64,{b64}"

KENDAL_FOOTER_LOGO_SVG = load_prefixed_svg("public/images/kendal-logo.svg", "kendal_ft_")
VANTI_LOGO_SVG = load_prefixed_svg("public/images/brands/vanti-logo.svg", "vanti_").replace('<svg ', '<svg class="vanti-brand-logo" ')
GLOBAL_LOGO_SVG = load_prefixed_svg("public/images/brands/global-logo.svg", "global_")
K2_LOGO_SVG = load_prefixed_svg("public/images/brands/k2-logo.svg", "k2_").replace('<svg ', '<svg class="k2-brand-logo" ')

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <title>{title_tr}</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 0;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background: #ffffff;
      color: #111827;
      margin: 0;
      padding: 0;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    .a4-page {{
      width: 210mm;
      height: 297mm;
      max-height: 297mm;
      padding: 12mm 15mm 10mm 15mm;
      box-sizing: border-box;
      display: flex;
      flex-direction: column;
      position: relative;
    }}

    /* 1. Header */
    .ubf-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 2px;
    }}
    
    /* Primary Brand Logo at Top-Left */
    .ubf-brand-main {{
      height: 72px;
      display: flex;
      align-items: center;
    }}
    .ubf-brand-main svg {{
      height: 50px;
      width: auto;
      max-width: 180px;
      display: block;
    }}
    .ubf-brand-main svg.vanti-brand-logo {{
      height: 70px !important;
      max-height: 70px !important;
      width: auto !important;
    }}
    .ubf-brand-main svg.k2-brand-logo {{
      height: 72px !important;
      max-height: 72px !important;
      width: auto !important;
    }}

    .ubf-header-right {{
      text-align: right;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
    }}
    .ubf-title-badge {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .ubf-accent-bar {{
      width: 4px;
      height: 40px;
      background: {accent_color};
      border-radius: 2px;
    }}
    .ubf-sheet-title {{
      font-size: 21px;
      font-weight: 800;
      color: #374151;
      letter-spacing: -0.3px;
      line-height: 1.1;
    }}
    .ubf-sheet-sub {{
      font-size: 11px;
      font-weight: 700;
      color: #6b7280;
      letter-spacing: 0.5px;
      margin-top: 2px;
      font-style: italic;
    }}

    /* 2. Hero: Title & Highlights on Left, Photo on Right */
    .ubf-hero {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 10px;
      margin-bottom: 12px;
      min-height: 115px;
    }}
    .ubf-hero-left {{
      flex: 1;
      padding-right: 28px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .ubf-prod-name-tr {{
      font-size: 18px;
      font-weight: 800;
      color: #0f172a;
      line-height: 1.25;
      letter-spacing: -0.2px;
      text-align: left;
    }}
    .ubf-prod-name-en {{
      font-size: 13.5px;
      font-weight: 600;
      color: #64748b;
      line-height: 1.25;
      margin-top: 3px;
      margin-bottom: 6px;
      text-align: left;
    }}
    .ubf-bullets {{
      list-style: none;
      margin-top: 4px;
    }}
    .ubf-bullets li {{
      font-size: 11.5px;
      color: #334155;
      font-weight: 500;
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .ubf-bullets li::before {{
      content: "•";
      color: {accent_color};
      font-size: 16px;
      line-height: 1;
    }}

    .ubf-hero-right {{
      width: 145px;
      height: 115px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 6px;
      flex-shrink: 0;
    }}
    .ubf-hero-right img {{
      max-width: 135px;
      max-height: 105px;
      object-fit: contain;
      filter: drop-shadow(0 3px 6px rgba(0,0,0,0.06));
    }}

    /* 4. Section Divider */
    .ubf-section-divider {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin-top: 12px;
      margin-bottom: 16px;
    }}
    .ubf-sec-marker {{
      width: 4.5px;
      height: 16px;
      background: {accent_color};
      border-radius: 1px;
    }}
    .ubf-sec-title {{
      font-size: 13px;
      font-weight: 800;
      color: #111827;
      letter-spacing: -0.1px;
      line-height: 1.1;
    }}
    .ubf-sec-line {{
      flex: 1;
      height: 1px;
      background: #cbd5e1;
    }}

    /* 5. 2-Row Specs Grid - GUARANTEES SAME HORIZONTAL ROW BASELINE */
    .ubf-specs-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      column-gap: 22px;
      margin-bottom: 14px;
      align-items: start;
    }}
    .ubf-specs-row:last-child {{
      margin-bottom: 6px;
    }}
    .ubf-spec-block {{
      margin-bottom: 0;
    }}
    .ubf-spec-head {{
      margin-bottom: 8px;
      border-left: 3.5px solid {accent_color};
      padding-left: 9px;
    }}
    .ubf-spec-head-en {{
      font-size: 13.5px;
      font-weight: 800;
      color: #0f172a;
      line-height: 1.2;
      letter-spacing: -0.1px;
    }}
    .ubf-spec-head-tr {{
      font-size: 10.5px;
      font-weight: 600;
      color: #64748b;
      margin-top: 2px;
    }}

    .ubf-table {{
      width: 100%;
      border-collapse: collapse;
    }}
    .ubf-table tr {{
      border-bottom: 1px solid #f1f5f9;
    }}
    .ubf-table td {{
      padding: 2.8px 0;
      font-size: 10.2px;
      line-height: 1.25;
    }}
    .ubf-table td.label-col {{
      color: #4b5563;
      font-weight: 500;
      width: 60%;
    }}
    .ubf-table td.value-col {{
      color: #0f172a;
      font-weight: 600;
      width: 40%;
    }}
    .energy-tag {{
      display: inline-block;
      font-weight: 900;
      color: #16a34a;
    }}

    /* 6. Drawing Box */
    .ubf-drawing-box {{
      height: 48px;
      margin: 4px 0 8px 0;
      display: flex;
      align-items: center;
      justify-content: flex-start;
      padding-left: 10px;
    }}
    .ubf-drawing-box img {{
      max-height: 46px;
      max-width: 200px;
      object-fit: contain;
    }}

    /* 7. SKU Table */
    .ubf-bottom-table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: auto;
      margin-bottom: 8px;
    }}
    .ubf-bottom-table thead th {{
      font-size: 8px;
      font-weight: 700;
      color: #1f2937;
      text-align: center;
      padding: 4px 3px;
      border-bottom: 1.5px solid #111827;
      background: #f8fafc;
      line-height: 1.1;
    }}
    .ubf-bottom-table thead th .th-sub {{
      display: block;
      font-size: 7px;
      color: #6b7280;
      font-weight: 500;
      margin-top: 1px;
    }}
    .ubf-bottom-table tbody td {{
      font-size: 8.5px;
      text-align: center;
      padding: 3.5px 3px;
      border-bottom: 1px solid #e5e7eb;
      color: #1f2937;
    }}
    .ubf-bottom-table tbody tr:last-child td {{
      border-bottom: 1.5px solid #111827;
    }}

    /* 8. Corporate Footer with Kendal Elektrik Manufacturer Info */
    .ubf-corporate-footer {{
      border-top: 1px solid #e2e8f0;
      padding-top: 5px;
      margin-top: 4px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 8.5px;
      color: #64748b;
    }}
    .ubf-footer-brand {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .ubf-footer-logo-badge {{
      background: #0f172a;
      padding: 3px 8px;
      border-radius: 4px;
      display: inline-flex;
      align-items: center;
    }}
    .ubf-footer-logo-badge svg {{
      height: 18px;
      width: auto;
      display: block;
    }}
    .ubf-footer-company {{
      font-weight: 700;
      color: #1e293b;
    }}
  </style>
</head>
<body>
  <div class="a4-page">
    <!-- Header: Primary Brand Logo at Top-Left (e.g. K2, Global, Vanti) -->
    <div class="ubf-header">
      <div class="ubf-brand-main">
        {brand_logo_svg}
      </div>

      <div class="ubf-header-right">
        <div class="ubf-title-badge">
          <div>
            <div class="ubf-sheet-title">ÜRÜN BİLGİ FORMU</div>
            <div class="ubf-sheet-sub">PRODUCT INFORMATION SHEET</div>
          </div>
          <div class="ubf-accent-bar"></div>
        </div>
      </div>
    </div>

    <!-- Hero: Title on Left, Product Photo on Right -->
    <div class="ubf-hero">
      <div class="ubf-hero-left">
        <div class="ubf-prod-name-tr">{title_tr}</div>
        <div class="ubf-prod-name-en">{title_en}</div>
      </div>
      <div class="ubf-hero-right">
        <img src="{prod_img_uri}" alt="{title_tr}">
      </div>
    </div>

    <!-- Section: Technical Specifications -->
    <div class="ubf-section-divider">
      <div class="ubf-sec-marker"></div>
      <div class="ubf-sec-title">Teknik Özellikler / Technical Specifications</div>
      <div class="ubf-sec-line"></div>
    </div>

    <!-- Row 1: Mechanical Specifications (Left) & Optical Specifications (Right) -->
    <div class="ubf-specs-row">
      <div class="ubf-spec-block">
        <div class="ubf-spec-head">
          <div class="ubf-spec-head-en">Mechanical Specifications</div>
          <div class="ubf-spec-head-tr">Mekanik Özellikler</div>
        </div>
        <table class="ubf-table">
          {mech_rows_html}
        </table>
      </div>

      <div class="ubf-spec-block">
        <div class="ubf-spec-head">
          <div class="ubf-spec-head-en">Optical Specifications</div>
          <div class="ubf-spec-head-tr">Optik Özellikler</div>
        </div>
        <table class="ubf-table">
          <tr><td class="label-col">Light Source / Işık Kaynağı</td><td class="value-col">{light_source}</td></tr>
          <tr><td class="label-col">Reflector / Reflektör</td><td class="value-col">{reflector}</td></tr>
          <tr><td class="label-col">Diffuser / Difüzör</td><td class="value-col">{diffuser}</td></tr>
          <tr><td class="label-col">CRI</td><td class="value-col">{cri}</td></tr>
          <tr><td class="label-col">Colour Temperature / Renk Sıcaklığı</td><td class="value-col">{cct}</td></tr>
          <tr><td class="label-col">Photobiological Risk / Fotobiyolojik Risk</td><td class="value-col">RG1</td></tr>
          <tr><td class="label-col">Beam Angle / Işık Açısı</td><td class="value-col">{beam}</td></tr>
        </table>
      </div>
    </div>

    <!-- Row 2: Electrical Specifications (Left) & Options (Right) - GUARANTEED EXACT SAME HORIZONTAL ROW BASELINE -->
    <div class="ubf-specs-row">
      <div class="ubf-spec-block">
        <div class="ubf-spec-head">
          <div class="ubf-spec-head-en">{spec_col1_title_en}</div>
          <div class="ubf-spec-head-tr">{spec_col1_title_tr}</div>
        </div>
        <table class="ubf-table">
          {spec_col1_rows_html}
        </table>
      </div>

      <div class="ubf-spec-block">
        <div class="ubf-spec-head">
          <div class="ubf-spec-head-en">{spec_col2_title_en}</div>
          <div class="ubf-spec-head-tr">{spec_col2_title_tr}</div>
        </div>
        <table class="ubf-table">
          {spec_col2_rows_html}
        </table>
      </div>
    </div>

    {drawing_section_html}

    <!-- SKU Table -->
    <table class="ubf-bottom-table">
      <thead>
        <tr>
          {table_headers_html}
        </tr>
      </thead>
      <tbody>
        {variant_rows_html}
      </tbody>
    </table>

    <!-- Corporate Footer: Kendal Elektrik Manufacturer Info -->
    <div class="ubf-corporate-footer">
      <div class="ubf-footer-brand">
        <div class="ubf-footer-logo-badge">
          {kendal_footer_logo_svg}
        </div>
        <div>
          <span class="ubf-footer-company">Kendal Elektrik A.Ş.</span> • Üretici Firma / Manufacturer
        </div>
      </div>
      <div>
        <span>www.kendalelektrik.com • info@kendalelektrik.com</span>
      </div>
    </div>
  </div>
</body>
</html>
"""

PRODUCTS = [
    {
        "filename": "K2_KBA742_Urun_Bilgi_Formu.pdf",
        "brand_name": "K2 Systems",
        "accent_color": "#ea580c",
        "brand_logo_svg": K2_LOGO_SVG,
        "prod_img": os.path.join(WORKSPACE, "public/images/urunler/kba742.webp"),
        "drawing_img": "",
        "title_tr": "KBA742 SENSÖRLÜ DUVAR APLİK",
        "title_en": "KBA742 SENSOR LED WALL LIGHT",
        "bullets": [],
        "body": "ABS",
        "ip": "IP65",
        "ik": "-",
        "ral": "9005 Siyah",
        "mounting": "Yüzey Montaj (Surface)",
        "light_source": "Filament Plastik",
        "reflector": "-",
        "diffuser": "Şeffaf PC",
        "cri": ">80",
        "cct": "2700K Sıcak Beyaz",
        "beam": "120°",
        "spec_col1_title_en": "Electrical & Solar Specifications",
        "spec_col1_title_tr": "Elektriksel & Solar Özellikler",
        "spec_col1_rows": [
            ("Solar Panel / Güneş Paneli", "Tek Kristalli (Monocrystal)"),
            ("Battery Type / Batarya", "Li-Ion 3.2V 400mAh"),
            ("Charge Time / Şarj Süresi", "6-8 Saat (Hours)"),
            ("Input Voltage / Giriş Gerilimi", "Şebeke Dışı (Solar DC)"),
            ("Photocell / Fotosel Sensör", "Evet (Yes)"),
            ("System Lifetime / Sistem Ömrü", ">20.000h"),
            ("Standards / Standartlar", "EN 60598-2-3"),
            ("Energy Class / Enerji Sınıfı", "<span class='energy-tag'>A</span>"),
        ],
        "spec_col2_title_en": "Options & Features",
        "spec_col2_title_tr": "Opsiyonlar & Ek Özellikler",
        "spec_col2_rows": [
            ("Charge Controller / Şarj Kontrol", "PWM Akıllı Kontrol"),
            ("DALI Dim", "-"),
            ("1-10V Dim", "-"),
            ("Emergency Kit / Acil Kit", "Entegre Solar Batarya"),
            ("Operating Temp. / Çalışma Sıcaklığı", "-10°C / +40°C"),
            ("Electrical Class / Elektriksel Sınıf", "Class III (SELV)"),
        ],
        "table_headers": ["Code No<span class='th-sub'>Ürün Kodu</span>", "Power<span class='th-sub'>Güç (W)</span>", "Luminous Flux<span class='th-sub'>Işık Akısı (lm)</span>", "Colour Temp.<span class='th-sub'>Renk Sıcaklığı (K)</span>", "Battery<span class='th-sub'>Batarya</span>", "Dimensions<span class='th-sub'>Boyutlar (cm)</span>", "Cut Size<span class='th-sub'>Kesim (mm)</span>", "Pcs/Pack<span class='th-sub'>Koli Adedi</span>", "Package Vol.<span class='th-sub'>Hacim (m3)</span>", "Weight<span class='th-sub'>Ağırlık (kg)</span>"],
        "variants": [
            ["KBA742", "5W Solar", "-", "2700K", "3.2V 1200mAh", "14x18x11 cm", "-", "50", "-", "-"]
        ]
    }
]

def generate_pdf(p):
    prod_img_uri = to_base64_data_uri(p["prod_img"])
    drawing_path = p.get("drawing_img", "")
    drawing_img_uri = to_base64_data_uri(drawing_path) if drawing_path and os.path.exists(drawing_path) else ""

    if drawing_img_uri:
        drawing_section_html = f'''
    <!-- Drawing -->
    <div class="ubf-section-divider">
      <div class="ubf-sec-marker"></div>
      <div class="ubf-sec-title">Technical Drawing / Teknik Çizim</div>
      <div class="ubf-sec-line"></div>
    </div>

    <div class="ubf-drawing-box">
      <img src="{drawing_img_uri}" alt="Teknik Çizim">
    </div>
'''
    else:
        drawing_section_html = ""

    bullets_html = "".join([f"<li>{b}</li>" for b in p["bullets"]])

    variant_rows = []
    for v in p["variants"]:
        cells = "".join([f"<td>{c}</td>" if i > 0 else f"<td><strong>{c}</strong></td>" for i, c in enumerate(v)])
        variant_rows.append(f"<tr>{cells}</tr>")

    spec_col1_rows_html = "".join([f"<tr><td class='label-col'>{r[0]}</td><td class='value-col'>{r[1]}</td></tr>" for r in p["spec_col1_rows"]])
    spec_col2_rows_html = "".join([f"<tr><td class='label-col'>{r[0]}</td><td class='value-col'>{r[1]}</td></tr>" for r in p["spec_col2_rows"]])
    table_headers_html = "".join([f"<th>{th}</th>" for th in p["table_headers"]])

    mech_items = [
        ("Body / Gövde", p.get("body", "")),
        ("IP Rating / IP Sınıfı", p.get("ip", "")),
        ("IK Rating Body / IK Gövde Sınıfı", p.get("ik", "")),
        ("Front Glass / Ön Cam", p.get("glass", "")),
        ("Cable Gland / Kablo Rakor", p.get("gland", "")),
        ("Cable / Kablo", p.get("cable", "")),
        ("RAL Code / Ral Kodu", p.get("ral", "")),
        ("Mounting Type / Montaj Tipi", p.get("mounting", "")),
        ("Fire Protection / Alev Koruması", p.get("fire", "")),
        ("Body Length / Gövde Boyu", p.get("length", "")),
    ]
    mech_rows_html = "".join([
        f"<tr><td class='label-col'>{lbl}</td><td class='value-col'>{val}</td></tr>"
        for lbl, val in mech_items if val and val != "-"
    ])

    html_content = HTML_TEMPLATE.format(
        title_tr=p["title_tr"],
        title_en=p["title_en"],
        brand_name=p["brand_name"],
        accent_color=p["accent_color"],
        brand_logo_svg=p["brand_logo_svg"],
        kendal_footer_logo_svg=KENDAL_FOOTER_LOGO_SVG,
        prod_img_uri=prod_img_uri,
        drawing_section_html=drawing_section_html,
        mech_rows_html=mech_rows_html,
        light_source=p["light_source"],
        reflector=p["reflector"],
        diffuser=p["diffuser"],
        cri=p["cri"],
        cct=p["cct"],
        beam=p["beam"],
        spec_col1_title_en=p["spec_col1_title_en"],
        spec_col1_title_tr=p["spec_col1_title_tr"],
        spec_col1_rows_html=spec_col1_rows_html,
        spec_col2_title_en=p["spec_col2_title_en"],
        spec_col2_title_tr=p["spec_col2_title_tr"],
        spec_col2_rows_html=spec_col2_rows_html,
        table_headers_html=table_headers_html,
        variant_rows_html="\n".join(variant_rows)
    )

    temp_html = os.path.join(OUT_DIR, p["filename"].replace(".pdf", ".html"))
    out_pdf = os.path.join(OUT_DIR, p["filename"])

    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f"--print-to-pdf={out_pdf}",
        f"file:///{temp_html}"
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(out_pdf):
        size = os.path.getsize(out_pdf)
        print(f"[OK] {p['filename']} ({size} bytes)")
    else:
        print(f"[ERR] Failed to create {p['filename']}: {res.stderr}")

if __name__ == "__main__":
    for prod in PRODUCTS:
        generate_pdf(prod)
    print("\nTum PDF'ler C:\\Users\\umutcan.celik\\Desktop\\UBF-Ornek-PDFler klasorune kaydedildi!")
