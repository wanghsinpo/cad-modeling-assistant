"""FCStd parser: extract feature tree, sketches, constraints, dimensions.
FCStd = zip containing Document.xml + shape data. We only need Document.xml.
"""
import zipfile
import xml.etree.ElementTree as ET
import json
import os
import re
from pathlib import Path
from collections import Counter, defaultdict


def parse_fcstd(path):
    """Return structured dict of the FreeCAD document."""
    try:
        with zipfile.ZipFile(path) as z:
            with z.open('Document.xml') as f:
                xml_data = f.read().decode('utf-8', errors='replace')
    except Exception as e:
        return {'error': str(e), 'path': str(path)}

    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        return {'error': f'XML parse: {e}', 'path': str(path)}

    objects = []
    for obj in root.iter('Object'):
        t = obj.get('type', '')
        n = obj.get('name', '')
        if t and n:
            objects.append({'type': t, 'name': n})

    # Extract ObjectData: properties per object
    obj_props = {}
    for od in root.iter('ObjectData'):
        for obj in od.findall('Object'):
            name = obj.get('name', '')
            props = {}
            for p in obj.iter('Property'):
                pname = p.get('name', '')
                ptype = p.get('type', '')
                # Find the value node
                for child in p:
                    val = child.get('value') or child.text or ''
                    # Collect all attributes as fallback
                    if not val and child.attrib:
                        val = dict(child.attrib)
                    props[pname] = {'type': ptype, 'value': val}
                    break
            obj_props[name] = props

    # Count feature types (PartDesign / Sketcher)
    type_counts = Counter(o['type'] for o in objects)

    # Extract sketch-level geometry & constraint summary
    sketches = []
    for obj in objects:
        if obj['type'] == 'Sketcher::SketchObject':
            name = obj['name']
            props = obj_props.get(name, {})
            sketches.append({'name': name, 'props_keys': list(props.keys())})

    # Extract dimensional-ish properties (Length, Radius, Angle, etc.)
    dims = []
    for name, props in obj_props.items():
        for pname, pv in props.items():
            if pv['type'] in ('App::PropertyLength', 'App::PropertyAngle',
                              'App::PropertyDistance', 'App::PropertyFloat',
                              'App::PropertyInteger') and isinstance(pv['value'], str):
                v = pv['value']
                try:
                    fv = float(v)
                    if 0 < abs(fv) < 10000:
                        dims.append({'obj': name, 'prop': pname, 'value': fv})
                except (ValueError, TypeError):
                    pass

    return {
        'path': str(path),
        'size': os.path.getsize(path),
        'objects': objects,
        'type_counts': dict(type_counts),
        'sketches_count': len(sketches),
        'dims_sample': dims[:30],
        'dims_count': len(dims),
    }


def classify_part(result):
    """Heuristic: classify by feature type counts."""
    tc = result.get('type_counts', {})
    names = [o['name'] for o in result.get('objects', [])]
    pad = tc.get('PartDesign::Pad', 0)
    pocket = tc.get('PartDesign::Pocket', 0)
    hole = tc.get('PartDesign::Hole', 0)
    revo = tc.get('PartDesign::Revolution', 0)
    polar = tc.get('PartDesign::PolarPattern', 0)
    linear = tc.get('PartDesign::LinearPattern', 0)
    fillet = tc.get('PartDesign::Fillet', 0)
    chamfer = tc.get('PartDesign::Chamfer', 0)
    mirror = tc.get('PartDesign::Mirrored', 0)
    sketch = tc.get('Sketcher::SketchObject', 0)

    tags = []
    if revo > 0:
        tags.append('revolution-based')
    if pad > 0:
        tags.append('prismatic')
    if polar > 0:
        tags.append('rotationally-symmetric')
    if linear > 0:
        tags.append('linear-array')
    if hole > 0:
        tags.append('threaded-holes')
    if chamfer > 0:
        tags.append('chamfered')
    if fillet > 0:
        tags.append('filleted')
    if mirror > 0:
        tags.append('mirror-symmetric')

    complexity = 'simple' if sketch <= 3 else ('medium' if sketch <= 8 else 'complex')
    tags.append(complexity)

    return tags


def feature_sequence(result):
    """Extract the ordered feature sequence (PartDesign chain)."""
    seq = []
    for o in result.get('objects', []):
        t = o['type']
        if t.startswith('PartDesign::') and t != 'PartDesign::Body':
            seq.append({'name': o['name'], 'type': t.replace('PartDesign::', '')})
        elif t == 'Sketcher::SketchObject':
            seq.append({'name': o['name'], 'type': 'Sketch'})
    return seq


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        r = parse_fcstd(sys.argv[1])
        r['tags'] = classify_part(r)
        r['sequence'] = feature_sequence(r)
        print(json.dumps(r, indent=2, default=str, ensure_ascii=False))
