import os
import shutil

def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    
    entry_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    if not os.path.exists(entry_src):
        raise FileNotFoundError(f"{entry_src} not found.")
        
    entry_dst = os.path.join(output_dir, "entry.png")
    shutil.copy2(entry_src, entry_dst)
    print(f"Successfully copied {entry_src} to {entry_dst}")

if __name__ == "__main__":
    main()
