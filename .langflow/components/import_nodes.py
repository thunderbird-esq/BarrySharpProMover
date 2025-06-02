import os
import json
import shutil

LANGFLOW_COMPONENTS_DIR = os.path.expanduser("~/.langflow/components")
SOURCE_COMPONENTS = os.path.join(os.path.dirname(__file__))

def install_components():
    if not os.path.exists(SOURCE_COMPONENTS):
        print("❌ Components folder not found.")
        return

    os.makedirs(LANGFLOW_COMPONENTS_DIR, exist_ok=True)

    for filename in os.listdir(SOURCE_COMPONENTS):
        src_path = os.path.join(SOURCE_COMPONENTS, filename)
        dst_path = os.path.join(LANGFLOW_COMPONENTS_DIR, filename)

        if os.path.isfile(src_path):
            shutil.copyfile(src_path, dst_path)
            print(f"✅ Imported: {filename}")

    print("🎉 All LangFlow nodes imported successfully.")

if __name__ == "__main__":
    install_components()