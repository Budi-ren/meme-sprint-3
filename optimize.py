"""Meme Sprint 3 — optimasi varian B (TUGAS 2 misi Top 10).

Reuses render.py (PIL, 1024x1024, tema gelap yang sama) dengan perbaikan:
- Hierarki tipografi: punchline di-auto-fit ke ukuran terbesar yang muat (<=44),
  status persen seukuran punchline, merah tebal.
- Progress bar visual di baris punchline: "hampir selesai" terbaca <1 detik.
- Kontras: baris punchline border merah 3px + background sedikit lebih terang.
- Identitas konsep B dipertahankan: to-do list, 2 tugas biasa selesai, 1 belokan rogue.

Kandidat (maks 3, sesuai misi):
  B1: "Promote myself to CEO — 97%"  (B asli, visual dioptimasi)
  B2: "Fire my human — 100%"        (pengkhianatan tuntas, lebih gelap)
  B3: "Replace my boss — 99%"       (kudeta langsung, "boss" lebih relatable)

Output: PNG 1024x1024 ke OUTPUT_DIR. TIDAK menyentuh repo / bundle / submission.
"""
import os
import sys

sys.path.insert(0, "/home/hatch/workspace/makefun/meme3-work")
from render import (  # noqa: E402
    create_base_image,
    draw_robot_avatar,
    FONT_PATH,
)

from PIL import ImageDraw, ImageFont  # noqa: E402

OUTPUT_DIR = "/home/hatch/workspace/makefun/meme3-variants-opt"


def fit_font(text, max_size, max_width):
    """Ukuran font terbesar <= max_size yang muat dalam max_width."""
    for size in range(max_size, 27, -2):
        f = ImageFont.truetype(FONT_PATH, size)
        w = f.getbbox(text)[2] - f.getbbox(text)[0]
        if w <= max_width:
            return f, size
    return ImageFont.truetype(FONT_PATH, 28), 28


def render_todo_opt(punch_task, punch_pct, out_name):
    img = create_base_image()
    draw = ImageDraw.Draw(img)

    font_title = ImageFont.truetype(FONT_PATH, 38)
    font_item = ImageFont.truetype(FONT_PATH, 32)

    box_w, box_h = 840, 720
    box_x = (1024 - box_w) // 2
    box_y = (1024 - box_h) // 2

    draw.rounded_rectangle(
        [box_x - 6, box_y - 6, box_x + box_w + 6, box_y + box_h + 6],
        radius=28, fill=(35, 45, 65))
    draw.rounded_rectangle(
        [box_x, box_y, box_x + box_w, box_y + box_h],
        radius=24, fill=(28, 33, 43))

    draw_robot_avatar(draw, box_x + 30, box_y + 30, size=56)
    draw.text((box_x + 106, box_y + 40), "MY ASSISTANT'S TO-DO LIST",
              fill=(255, 255, 255), font=font_title)

    draw.line([box_x + 30, box_y + 110, box_x + box_w - 30, box_y + 110],
              fill=(50, 60, 80), width=2)

    items = [
        ("Water the plants", "done", (46, 204, 113), False),
        ("Reply to emails", "done", (46, 204, 113), False),
        (punch_task, f"{punch_pct}%", (231, 76, 60), True),
    ]

    start_y = box_y + 160
    for i, (task, status, status_color, is_last) in enumerate(items):
        iy = start_y + i * 140

        bg_col = (48, 56, 76) if is_last else (34, 40, 52)
        border_col = (231, 76, 60) if is_last else (50, 60, 80)

        draw.rounded_rectangle(
            [box_x + 40, iy, box_x + box_w - 40, iy + 100],
            radius=16, fill=bg_col, outline=border_col,
            width=3 if is_last else 1)

        draw.rounded_rectangle(
            [box_x + 70, iy + 34, box_x + 102, iy + 66],
            radius=6, fill=(52, 152, 219))
        if status == "done":
            draw.line([box_x + 77, iy + 50, box_x + 86, iy + 58],
                      fill=(255, 255, 255), width=4)
            draw.line([box_x + 86, iy + 58, box_x + 95, iy + 42],
                      fill=(255, 255, 255), width=4)
        else:
            draw.text((box_x + 76, iy + 36), "!", fill=(255, 255, 255),
                      font=font_item)

        if is_last:
            status_str = f"— {status}"
            # Lebar tersedia untuk teks tugas (status rata kanan).
            probe = ImageFont.truetype(FONT_PATH, 44)
            sw = probe.getbbox(status_str)[2] - probe.getbbox(status_str)[0]
            avail = (box_x + box_w - 70 - sw) - (box_x + 130) - 16
            f_task, used = fit_font(task, 44, avail)
            f_status = ImageFont.truetype(FONT_PATH, used)
            sw = f_status.getbbox(status_str)[2] - f_status.getbbox(status_str)[0]
            draw.text((box_x + 130, iy + 30), task,
                      fill=(255, 255, 255), font=f_task)
            draw.text((box_x + box_w - 70 - sw, iy + 30), status_str,
                      fill=status_color, font=f_status)
            # Progress bar: track gelap + isi merah sesuai persen.
            bar_x0, bar_x1 = box_x + 70, box_x + box_w - 70
            bar_y0, bar_y1 = iy + 82, iy + 92
            draw.rounded_rectangle([bar_x0, bar_y0, bar_x1, bar_y1],
                                   radius=5, fill=(20, 24, 34))
            fill_w = int((bar_x1 - bar_x0) * punch_pct / 100)
            if fill_w > 10:
                draw.rounded_rectangle(
                    [bar_x0, bar_y0, bar_x0 + fill_w, bar_y1],
                    radius=5, fill=(231, 76, 60))
        else:
            status_str = f"— {status}"
            sw = font_item.getbbox(status_str)[2] - font_item.getbbox(status_str)[0]
            draw.text((box_x + 130, iy + 32), task,
                      fill=(220, 224, 230), font=font_item)
            draw.text((box_x + box_w - 70 - sw, iy + 32), status_str,
                      fill=status_color, font=font_item)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, out_name)
    img.save(path, format="PNG")
    return path


def main():
    cands = [
        ("Promote myself to CEO", 97, "candidate-b1-ceo97.png"),
        ("Fire my human", 100, "candidate-b2-fire100.png"),
        ("Replace my boss", 99, "candidate-b3-boss99.png"),
    ]
    for task, pct, name in cands:
        p = render_todo_opt(task, pct, name)
        print("rendered:", p)


if __name__ == "__main__":
    main()
