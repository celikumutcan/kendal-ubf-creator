import os
import re
import zipfile
import json
import xml.etree.ElementTree as ET

def clean_txt(t):
    if not t:
        return ""
    # remove weird docx coordinate strings like 3804285392430000 or left366322500
    t = re.sub(r'^(left|center|right)?\d{10,25}', '', t)
    t = re.sub(r'\d{10,25}', '', t)
    return t.strip()

def parse_docx_ubf(docx_path):
    with zipfile.ZipFile(docx_path, 'r') as z:
        xml_content = z.read('word/document.xml')
        root = ET.fromstring(xml_content)

        paras = []
        for p in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            raw = ''.join(p.itertext()).strip()
            cleaned = clean_txt(raw)
            if cleaned:
                paras.append(cleaned)

        # Extract embedded media images
        media_names = [m for m in z.namelist() if m.startswith('word/media/')]

    result = {
        'source_file': os.path.basename(docx_path),
        'media_count': len(media_names),
        'model': '',
        'nameTr': '',
        'nameEn': '',
        'bullets': [],
        'body': 'Metal',
        'ip': 'IP40',
        'ik': 'IK06',
        'fire': '-',
        'ral': '9016',
        'mounting': 'Sıva Altı',
        'volt': '220-240Vac',
        'freq': '50-60Hz',
        'classVal': 'Class II',
        'life': '>20.000h',
        'pf': '>0,50',
        'temp': '-10°C / +40°C',
        'standards': 'IEC60598-2-1 and EN62031',
        'energy': 'F',
        'lightSource': 'SMD LED',
        'diffuser': 'PMMA',
        'cri': '>80',
        'beam': '120°',
        'cct': '3000K/4000K/6500K',
        'bio': 'RG1',
        'variants': []
    }

    # Model code from filename
    fn = os.path.basename(docx_path)
    model_match = re.match(r'^([A-Z0-9]+)', fn)
    if model_match:
        result['model'] = model_match.group(1)

    # Detect Titles (usually around indices 1-8)
    for p in paras[:8]:
        if 'ÜRÜN BİLGİ FORMU' in p or 'PRODUCT INFORMATION' in p or 'Marka' in p:
            continue
        # Check if model or any digit part is in title, or if it's an uppercase product header
        has_model = result['model'] and (result['model'] in p or result['model'][-3:] in p or '_' in p)
        if has_model or (len(p) > 5 and p.isupper() and any(c.isalpha() for c in p)):
            if not result['nameTr']:
                result['nameTr'] = p
            elif not result['nameEn'] and p != result['nameTr']:
                result['nameEn'] = p
                break

    # If dual title in one line (e.g. GES230_234 TORCH LED AMPUL   GES230_234 LED TORCH BULB)
    if result['nameTr'] and not result['nameEn'] and '   ' in result['nameTr']:
        parts = [p.strip() for p in re.split(r'\s{3,}', result['nameTr']) if p.strip()]
        if len(parts) >= 2:
            result['nameTr'] = parts[0]
            result['nameEn'] = parts[1]

    # Bullets
    for p in paras[4:12]:
        if any(w in p for w in ['design', 'driver', 'Panel', 'Gövde', 'IP', 'Marka', 'Brand', 'Mekanik']):
            if 'design' in p or 'driver' in p or 'Batarya' in p or 'Sensor' in p or 'Sensör' in p:
                result['bullets'].append(p)

    # Full text search for specs
    full_text = ' \n '.join(paras)

    # IP Rating
    ip_m = re.search(r'IP\s*(\d{2})', full_text, re.IGNORECASE)
    if ip_m:
        result['ip'] = f"IP{ip_m.group(1)}"

    # IK Rating
    ik_m = re.search(r'IK\s*(\d{2})', full_text, re.IGNORECASE)
    if ik_m:
        result['ik'] = f"IK{ik_m.group(1)}"

    # Energy Class
    en_m = re.search(r'Energy\s*Class\s*(?:Enerji\s*Sınıfı)?\s*([A-G])', full_text, re.IGNORECASE)
    if en_m:
        result['energy'] = en_m.group(1).upper()

    # Voltage
    v_m = re.search(r'(220\s*-\s*240\s*V?\s*AC|12V|24V|220-240Vac)', full_text, re.IGNORECASE)
    if v_m:
        result['volt'] = v_m.group(1)

    # Frequency
    f_m = re.search(r'(50\s*-\s*60\s*Hz)', full_text, re.IGNORECASE)
    if f_m:
        result['freq'] = f_m.group(1)

    # Variant table rows (look for lines ending with numbers or dimensions)
    table_rows = []
    for p in paras[30:]:
        # Pattern like: MODEL 25W 2300lm 3000K 92 30*30 ...
        tokens = [t.strip() for t in re.split(r'\s{2,}', p) if t.strip()]
        if len(tokens) >= 5 and any(result['model'] in t for t in tokens):
            row = {
                'code': tokens[0] if len(tokens) > 0 else result['model'],
                'power': tokens[1] if len(tokens) > 1 else '',
                'lumen': tokens[2] if len(tokens) > 2 else '',
                'cct': tokens[3] if len(tokens) > 3 else '',
                'eff': tokens[4] if len(tokens) > 4 else '',
                'dim': tokens[5] if len(tokens) > 5 else '',
                'cut': tokens[6] if len(tokens) > 6 else '-',
                'pcs': tokens[7] if len(tokens) > 7 else '',
                'vol': tokens[8] if len(tokens) > 8 else '',
                'weight': tokens[9] if len(tokens) > 9 else '-'
            }
            table_rows.append(row)

    if table_rows:
        result['variants'] = table_rows
    else:
        # Fallback 1 default row
        result['variants'] = [{
            'code': result['model'],
            'power': '25W',
            'lumen': '2300lm',
            'cct': '4000K',
            'eff': '92',
            'dim': '-',
            'cut': '-',
            'pcs': '10',
            'vol': '-',
            'weight': '-'
        }]

    return result

if __name__ == '__main__':
    folder = r'C:\Users\umutcan.celik\Desktop\web sayfası projesi\Ahmet Bey den aldığım Ürün Bilgi Formları\Ürün Bilgi Formları - Enerji Sınıfı Çalışması\Enerji Sınıfı Eklenen Formlar (353 Adet)'
    samples = ['GDL414 Ürün Bilgi Formu.docx', 'GES230 Ürün Bilgi Formu.docx', 'KBA742 Ürün Bilgi Formu.docx']

    for s in samples:
        path = os.path.join(folder, s)
        if os.path.exists(path):
            data = parse_docx_ubf(path)
            print(f"=== PARSED {s} ===")
            print(json.dumps(data, indent=2, ensure_ascii=False))
