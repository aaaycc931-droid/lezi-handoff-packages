"""Compare raster pixels without editing, scaling, or regenerating images."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('candidate', type=Path)
    parser.add_argument('--regions', type=Path, required=True)
    parser.add_argument('--mask', type=Path, help='Binary L/1 PNG: white pixels allow changes; black pixels protect.')
    parser.add_argument('--expected-source-sha256', help='Previously recorded approved source digest.')
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    source_hash = digest(args.source)
    candidate_hash = digest(args.candidate)
    if args.expected_source_sha256 and source_hash != args.expected_source_sha256:
        raise SystemExit('Source differs from the recorded approved digest.')
    with Image.open(args.source) as a, Image.open(args.candidate) as b:
        supported = {'1', 'L', 'LA', 'P', 'RGB', 'RGBA'}
        if a.mode not in supported or b.mode not in supported:
            raise SystemExit('Unsupported precision or color mode; do not silently downconvert.')
        if a.size != b.size:
            raise SystemExit('Dimensions differ; no automatic resizing is permitted.')
        width, height = a.size
        regions = json.loads(args.regions.read_text())['regions']
        for region in regions:
            values = [region[key] for key in ('x', 'y', 'width', 'height')]
            if any(type(value) is not int for value in values):
                raise SystemExit('Region coordinates must be integer pixels.')
            x, y, w, h = values
            if min(x, y) < 0 or min(w, h) <= 0 or x+w > width or y+h > height:
                raise SystemExit('Region outside image or empty.')
        allowed = bytearray(width * height)
        for region in regions:
            x, y, w, h = (region[key] for key in ('x', 'y', 'width', 'height'))
            for row in range(y, y+h):
                allowed[row*width+x:row*width+x+w] = b'\x01' * w
        if args.mask:
            with Image.open(args.mask) as mask:
                if mask.size != a.size or mask.mode not in {'1', 'L'}:
                    raise SystemExit('Mask must be binary L/1 at the original image dimensions.')
                for index, value in enumerate(mask.convert('L').tobytes()):
                    if value not in (0, 255):
                        raise SystemExit('Mask must contain only 0 and 255; no implicit thresholding.')
                    allowed[index] = allowed[index] and value == 255
        changed = outside = 0
        first_outside = None
        rgba_a, rgba_b = a.convert('RGBA'), b.convert('RGBA')
        pixels_a = rgba_a.get_flattened_data() if hasattr(rgba_a, 'get_flattened_data') else rgba_a.getdata()
        pixels_b = rgba_b.get_flattened_data() if hasattr(rgba_b, 'get_flattened_data') else rgba_b.getdata()
        for index, (pixel_a, pixel_b) in enumerate(zip(pixels_a, pixels_b)):
            if pixel_a != pixel_b:
                changed += 1
                if not allowed[index]:
                    outside += 1
                    if first_outside is None:
                        first_outside = [index % width, index // width]
        result = {
            'source_sha256': source_hash,
            'candidate_sha256': candidate_hash,
            'width': width,
            'height': height,
            'regions': regions,
            'changed_pixels': changed,
            'changed_pixels_outside_authorized_regions': outside,
            'first_outside_pixel': first_outside,
            'source_file_unchanged_during_check': digest(args.source) == source_hash,
            'candidate_file_unchanged_during_check': digest(args.candidate) == candidate_hash,
            'recorded_source_digest_checked': bool(args.expected_source_sha256),
            'mask_used': bool(args.mask),
            'comparison_precision': 'decoded 8-bit RGBA; not original encoded bytes',
            'color_profile_unchanged': all(a.info.get(key) == b.info.get(key)
                for key in ('icc_profile', 'srgb', 'gamma', 'chromaticity')),
            'pixel_preservation': 'passed' if outside == 0 else 'failed',
            'visual_quality': 'not_assessed_by_this_script',
        }
        result['verification_passed'] = (outside == 0 and result['color_profile_unchanged']
            and result['source_file_unchanged_during_check'] and result['candidate_file_unchanged_during_check'])
    output = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.out:
        args.out.write_text(output)
    print(output)
    return 0 if result['verification_passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
