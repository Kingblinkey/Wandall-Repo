import os
import hashlib
import zipfile

def build_repo_manifests():
    root = "."
    zips_dir = "zips"
    
    addons = []
    
    # Scan subdirectories under zips/ for addon.xml
    for item in sorted(os.listdir(zips_dir)):
        sub = os.path.join(zips_dir, item)
        if os.path.isdir(sub):
            ax = os.path.join(sub, "addon.xml")
            if os.path.exists(ax):
                with open(ax, "r", encoding="utf-8") as f:
                    xml_text = f.read()
                clean = xml_text.split("?>")[-1].strip()
                addons.append(clean)
                
    content = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<addons>\n"
    content += "\n".join(addons)
    content += "\n</addons>\n"
    
    md5_hash = hashlib.md5(content.encode("utf-8")).hexdigest()
    
    # Write to root
    with open("addons.xml", "w", encoding="utf-8") as f:
        f.write(content)
    with open("addons.xml.md5", "w", encoding="utf-8") as f:
        f.write(md5_hash)
        
    # Write to zips/
    with open(os.path.join(zips_dir, "addons.xml"), "w", encoding="utf-8") as f:
        f.write(content)
    with open(os.path.join(zips_dir, "addons.xml.md5"), "w", encoding="utf-8") as f:
        f.write(md5_hash)
        
    print(f"Updated addons.xml and addons.xml.md5 (MD5: {md5_hash})")

if __name__ == "__main__":
    build_repo_manifests()
