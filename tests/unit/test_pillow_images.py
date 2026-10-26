from PIL import Image

from browser_harness import video_render


def test_masked_frame_redacts_scaled_pixels_without_changing_source(tmp_path):
    source = tmp_path / "frame.png"
    Image.new("RGB", (200, 100), "red").save(source)
    composition = {
        "viewport": {"w": 100, "h": 50},
        "redact": {"frame.png": [
            {"x": 10, "y": 10, "w": 20, "h": 10,
             "pad": 0, "radius": 0, "fill": "black", "stroke": ""},
        ]},
    }

    result = video_render.masked_frame(tmp_path, composition, "frame.png")

    assert result.size == (200, 100)
    assert result.getpixel((40, 30)) == (0, 0, 0)
    assert result.getpixel((5, 5)) == (255, 0, 0)
    with Image.open(source) as original:
        assert original.getpixel((40, 30)) == (255, 0, 0)


def test_contact_sheet_scales_transparent_capture_and_renders_labels(tmp_path):
    source = tmp_path / "capture.png"
    output = tmp_path / "sheet.png"
    Image.new("RGBA", (800, 400), (255, 0, 0, 128)).save(source)

    video_render.contact_sheet(
        [{"path": str(source), "label": "capture", "time": 1.25}],
        output,
        "Review",
    )

    with Image.open(output) as sheet:
        assert sheet.mode == "RGB"
        assert sheet.size == (1640, 317)
        assert sheet.getpixel((208, 100)) == (255, 0, 0)
        assert sheet.getpixel((500, 100)) == (23, 26, 32)


