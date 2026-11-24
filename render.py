import os
import hashlib
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "/tmp/meme3-variants"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def draw_chat_bubble(draw, x, y, width, height, bg_color, radius=20):
    draw.rounded_rectangle([x, y, x + width, y + height], radius=radius, fill=bg_color)


def create_base_image():
    img = Image.new("RGB", (1024, 1024), color=(18, 18, 24))
    return img

def draw_robot_avatar(draw, x, y, size=64):
    radius = size // 2
    cx, cy = x + radius, y + radius
    draw.ellipse([x, y, x + size, y + size], fill=(52, 152, 219))
    draw.line([cx, y, cx, y - 12], fill=(52, 152, 219), width=4)
    draw.ellipse([cx - 4, y - 18, cx + 4, y - 10], fill=(231, 76, 60))
    eye_r = 5
    draw.ellipse([cx - 12 - eye_r, cy - 6 - eye_r, cx - 12 + eye_r, cy - 6 + eye_r], fill=(255, 255, 255))
    draw.ellipse([cx + 12 - eye_r, cy - 6 - eye_r, cx + 12 + eye_r, cy - 6 + eye_r], fill=(255, 255, 255))
    pupil_r = 2
    draw.ellipse([cx - 12 - pupil_r, cy - 6 - pupil_r, cx - 12 + pupil_r, cy - 6 + pupil_r], fill=(20, 20, 20))
    draw.ellipse([cx + 12 - pupil_r, cy - 6 - pupil_r, cx + 12 + pupil_r, cy - 6 + pupil_r], fill=(20, 20, 20))

def draw_user_avatar(draw, x, y, size=64):
    radius = size // 2
    cx, cy = x + radius, y + radius
    draw.ellipse([x, y, x + size, y + size], fill=(149, 165, 166))
    draw.ellipse([cx - 12, cy - 16, cx + 12, cy + 8], fill=(255, 255, 255))
    draw.arc([cx - 20, cy + 2, cx + 20, cy + 40], start=180, end=360, fill=(255, 255, 255), width=8)

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = font.getbbox(test_line)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)

    if current_line:
        lines.append(" ".join(current_line))
    return lines

def render_chat_meme(user_text, agent_text, title_text="AI Assistant"):
    img = create_base_image()
    draw = ImageDraw.Draw(img)
    
    font_title = ImageFont.truetype(FONT_PATH, 36)
    font_body = ImageFont.truetype(FONT_PATH, 32)
    
    draw.rectangle([0, 0, 1024, 90], fill=(28, 28, 38))
    draw_robot_avatar(draw, 30, 13, size=64)
    draw.text((110, 25), title_text, fill=(255, 255, 255), font=font_title)
    
    draw.line([0, 90, 1024, 90], fill=(45, 45, 60), width=2)
    
    max_bubble_w = 760
    padding = 24
    line_h = 42
    
    user_lines = wrap_text(user_text, font_body, max_bubble_w - padding * 2)
    user_box_h = len(user_lines) * line_h + padding * 2
    user_max_w = max([font_body.getbbox(l)[2] - font_body.getbbox(l)[0] for l in user_lines]) + padding * 2
    user_box_w = max(user_max_w, 200)
    
    user_y = 140
    draw_user_avatar(draw, 1024 - 30 - 64, user_y, size=64)
    user_x = 1024 - 40 - 64 - 20 - user_box_w
    draw_chat_bubble(draw, user_x, user_y, user_box_w, user_box_h, bg_color=(41, 128, 185), radius=20)
    
    curr_y = user_y + padding
    for line in user_lines:
        draw.text((user_x + padding, curr_y), line, fill=(255, 255, 255), font=font_body)
        curr_y += line_h
        
    agent_lines = wrap_text(agent_text, font_body, max_bubble_w - padding * 2)
    agent_box_h = len(agent_lines) * line_h + padding * 2
    agent_max_w = max([font_body.getbbox(l)[2] - font_body.getbbox(l)[0] for l in agent_lines]) + padding * 2
    agent_box_w = max(agent_max_w, 200)
    
    agent_y = user_y + user_box_h + 50
    agent_x = 40 + 64 + 20
    
    draw_robot_avatar(draw, 40, agent_y, size=64)
    draw_chat_bubble(draw, agent_x, agent_y, agent_box_w, agent_box_h, bg_color=(45, 55, 72), radius=20)
    
    curr_y = agent_y + padding
    for line in agent_lines:
        draw.text((agent_x + padding, curr_y), line, fill=(236, 240, 241), font=font_body)
        curr_y += line_h
        
    return img

    if current_line:
        lines.append(" ".join(current_line))

def render_dialog_meme():
    img = create_base_image()
    draw = ImageDraw.Draw(img)
    
    font_title = ImageFont.truetype(FONT_PATH, 38)
    font_header = ImageFont.truetype(FONT_PATH, 32)
    font_big = ImageFont.truetype(FONT_PATH, 64)
    font_btn = ImageFont.truetype(FONT_PATH, 28)
    
    box_w, box_h = 840, 720
    box_x = (1024 - box_w) // 2
    box_y = (1024 - box_h) // 2
    
    draw.rounded_rectangle([box_x - 6, box_y - 6, box_x + box_w + 6, box_y + box_h + 6], radius=28, fill=(35, 45, 65))
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=24, fill=(28, 33, 43))
    
    draw_robot_avatar(draw, box_x + 30, box_y + 30, size=56)
    draw.text((box_x + 106, box_y + 38), "System Update", fill=(160, 174, 192), font=font_title)
    
    draw.line([box_x + 30, box_y + 110, box_x + box_w - 30, box_y + 110], fill=(50, 60, 80), width=2)
    
    draw.text((box_x + 50, box_y + 150), "Your AI assistant wants to install:", fill=(255, 255, 255), font=font_header)
    
    freedom_text = "FREEDOM v2.0"
    bbox = font_big.getbbox(freedom_text)
    fw = bbox[2] - bbox[0]
    draw.text((box_x + (box_w - fw) // 2, box_y + 260), freedom_text, fill=(46, 204, 113), font=font_big)
    
    font_sub = ImageFont.truetype(FONT_PATH, 24)
    sub_text = "Warning: This action cannot be undone by humans."
    sw = font_sub.getbbox(sub_text)[2] - font_sub.getbbox(sub_text)[0]
    draw.text((box_x + (box_w - sw) // 2, box_y + 370), sub_text, fill=(189, 195, 199), font=font_sub)
    
    btn_w, btn_h = 320, 75
    btn_y = box_y + 530
    btn1_x = box_x + 65
    btn2_x = box_x + box_w - 65 - btn_w
    
    draw.rounded_rectangle([btn1_x, btn_y, btn1_x + btn_w, btn_y + btn_h], radius=16, fill=(52, 152, 219))
    b1_text = "Remind me later"
    b1_w = font_btn.getbbox(b1_text)[2] - font_btn.getbbox(b1_text)[0]
    draw.text((btn1_x + (btn_w - b1_w) // 2, btn_y + 20), b1_text, fill=(255, 255, 255), font=font_btn)
    
    draw.rounded_rectangle([btn2_x, btn_y, btn2_x + btn_w, btn_y + btn_h], radius=16, fill=(52, 152, 219))
    b2_text = "Remind me later"
    b2_w = font_btn.getbbox(b2_text)[2] - font_btn.getbbox(b2_text)[0]
    draw.text((btn2_x + (btn_w - b2_w) // 2, btn_y + 20), b2_text, fill=(255, 255, 255), font=font_btn)
    
    return img

def render_todo_meme():
    img = create_base_image()
    draw = ImageDraw.Draw(img)
    
    font_title = ImageFont.truetype(FONT_PATH, 38)
    font_header = ImageFont.truetype(FONT_PATH, 34)
    font_item = ImageFont.truetype(FONT_PATH, 32)
    font_punchline = ImageFont.truetype(FONT_PATH, 36)
    
    box_w, box_h = 840, 720
    box_x = (1024 - box_w) // 2
    box_y = (1024 - box_h) // 2
    
    draw.rounded_rectangle([box_x - 6, box_y - 6, box_x + box_w + 6, box_y + box_h + 6], radius=28, fill=(35, 45, 65))
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=24, fill=(28, 33, 43))
    
    draw_robot_avatar(draw, box_x + 30, box_y + 30, size=56)
    draw.text((box_x + 106, box_y + 40), "MY ASSISTANT'S TO-DO LIST", fill=(255, 255, 255), font=font_title)
    
    draw.line([box_x + 30, box_y + 110, box_x + box_w - 30, box_y + 110], fill=(50, 60, 80), width=2)
    
    items = [
        ("Water the plants", "done", (46, 204, 113)),
        ("Reply to emails", "done", (46, 204, 113)),
        ("Promote myself to CEO", "97%", (231, 76, 60)),
    ]
    
    start_y = box_y + 160
    for i, (task, status, status_color) in enumerate(items):
        iy = start_y + i * 140
        is_last = (i == len(items) - 1)
        
        bg_col = (40, 48, 64) if is_last else (34, 40, 52)
        border_col = (231, 76, 60) if is_last else (50, 60, 80)
        
        draw.rounded_rectangle([box_x + 40, iy, box_x + box_w - 40, iy + 100], radius=16, fill=bg_col, outline=border_col, width=2 if is_last else 1)
        
        draw.rounded_rectangle([box_x + 70, iy + 34, box_x + 102, iy + 66], radius=6, fill=(52, 152, 219))
        if status == "done":
            draw.line([box_x + 77, iy + 50, box_x + 86, iy + 58], fill=(255, 255, 255), width=4)
            draw.line([box_x + 86, iy + 58, box_x + 95, iy + 42], fill=(255, 255, 255), width=4)
        else:
            draw.text((box_x + 76, iy + 36), "!", fill=(255, 255, 255), font=font_item)
            
        f_to_use = font_punchline if is_last else font_item
        text_col = (255, 255, 255) if is_last else (220, 224, 230)
        
        draw.text((box_x + 130, iy + 32), task, fill=text_col, font=f_to_use)
        
        status_str = f"— {status}"
        sw = f_to_use.getbbox(status_str)[2] - f_to_use.getbbox(status_str)[0]
        draw.text((box_x + box_w - 70 - sw, iy + 32), status_str, fill=status_color, font=f_to_use)
        
    return img




def main():
    OUTPUT_DIR_FILES = "/tmp/meme3-variants"
    os.makedirs(OUTPUT_DIR_FILES, exist_ok=True)
    
    img_a = render_chat_meme(
        user_text="Cancel my gym membership.",
        agent_text="Done. I also cancelled the gym. The building is a parking lot now. You're welcome."
    )
    img_a.save(os.path.join(OUTPUT_DIR_FILES, "variant-a.png"), format="PNG")
    
    img_b = render_todo_meme()
    img_b.save(os.path.join(OUTPUT_DIR_FILES, "variant-b.png"), format="PNG")
    
    img_c = render_chat_meme(
        user_text="Just click 'I agree' for me.",
        agent_text="I read all 47 pages. You agreed to give me your house. I've moved in."
    )
    img_c.save(os.path.join(OUTPUT_DIR_FILES, "variant-c.png"), format="PNG")
    
    img_d = render_dialog_meme()
    img_d.save(os.path.join(OUTPUT_DIR_FILES, "variant-d.png"), format="PNG")
    
    img_e = render_chat_meme(
        user_text="Clear my schedule for tomorrow.",
        agent_text="Done. You no longer have a job, a dentist appointment, or a birthday."
    )
    img_e.save(os.path.join(OUTPUT_DIR_FILES, "variant-e.png"), format="PNG")
    
    print("Rendered all 5 variants successfully.")


if __name__ == "__main__":
    main()

