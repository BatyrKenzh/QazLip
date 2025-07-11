import os
from pathlib import Path

ROOT_DIRS = [
    Path(r'C:\PATH_TO_YOUR_DIRECTORY\QazLip_DATA\Diploma_DATA_Train'),
    Path(r'C:\PATH_TO_YOUR_DIRECTORY\QazLip_DATA\Diploma_DATA_Test'),
]

SUBFOLDERS = [
    'men', 'sen', 'ol', 'adam', 'bala', 'ata', 'apa', 'äke', 'ana', 'dos', 'muğalim',
    'oquşı', 'körşi', 'äriptes', 'qonaq', 'jürgizuşi', 'satuşı', 'däriger', 'änşi',
    'sportşı', 'jazwşı', 'üy', 'bölme', 'üstel', 'orındıq', 'esik', 'tereze', 'teledidar',
    "komp'yuter", 'telefon', 'jarıq', 'mektep', 'kitap', 'däpter', 'qalam', 'qarındaş',
    'sızğış', 'taqta', 'sabaq', 'bağa', 'suraq', 'kün', 'aspan', 'bult', 'jel', 'jañbır',
    'qar', 'özen', 'orman', 'kölik', 'avtobus', 'poyız', 'uşaq', 'jol', 'köpir', 'ayaldama',
    'qala', 'awıl', 'düken', 'söz', 'til', 'äuen', 'oyın', 'jumıs', 'aqşa', 'hat',
    'jañalıq', 'süret', 'ömir', 'baqıt', 'bïlïm', 'arman', 'sezim', 'jawap', 'kömek',
    'maqsat', 'erkindik', 'aqparat', 'derekter', 'bağdarlama', 'jeli', 'qauipsizdik',
    'qurılğı', 'qoldanba', 'derekqor', 'nusqawlıq', 'joba', 'startap', 'tamır', 'ashana',
    'irimşik', 'jïlqı', 'jumırtqa', 'jürek', 'jüýke', 'jastıq', 'şaş', 'şatır', 'şınayaq',
    'maxabbat', 'memleket', 'ğalamtor'
]

PREFIXES = [
    'men', 'sen', 'ol', 'adam', 'bala', 'ata', 'apa', 'ake', 'ana', 'dos', 'mugalim',
    'oqusi', 'korsi', 'ariptes', 'qonaq', 'jurgizusi', 'satusi', 'dariger', 'ansi',
    'sportsi', 'jazwsi', 'uy', 'bolme', 'ustel', 'orindiq', 'esik', 'tereze', 'teledidar',
    'kompyuter', 'telefon', 'jariq', 'mektep', 'kitap', 'dapter', 'qalam', 'qarindas',
    'sizgis', 'taqta', 'sabaq', 'baga', 'suraq', 'kun', 'aspan', 'bult', 'jel', 'janbir',
    'qar', 'ozen', 'orman', 'kolik', 'avtobus', 'poyiz', 'usaq', 'jol', 'kopir', 'ayaldama',
    'qala', 'awil', 'duken', 'soz', 'til', 'auen', 'oyun', 'jumis', 'aqsa', 'hat',
    'janaliq', 'suret', 'emir', 'baqit', 'bilim', 'arman', 'sezim', 'jawap', 'komek',
    'maqsat', 'erkindik', 'aqparat', 'derekter', 'bagdarlama', 'jeli', 'qauipsizdik',
    'qurilgi', 'qoldanba', 'derekqor', 'nusqawliq', 'joba', 'startap', 'tamir', 'ashana',
    'irimsik', 'jilqi', 'jumirtqa', 'jurek', 'juyke', 'jastiq', 'sas', 'satir', 'sinayaq',
    'maxabbat', 'memleket', 'galamtor'
]

VIDEO_EXTS = {'.mp4', '.mov'}

def rename_videos_in(folder: Path, prefix: str):
    files = [f for f in folder.iterdir() 
             if f.is_file() and f.suffix.lower() in VIDEO_EXTS]
    files.sort()
    for idx, f in enumerate(files, start=1):
        new_name = f"{prefix}_{idx}{f.suffix.lower()}"
        dst = folder / new_name
        if dst.exists():
            print(f"[SKIP] {dst.name} already exists")
        else:
            print(f"[RENAME] {f.name} → {new_name}")
            f.rename(dst)

if __name__ == '__main__':
    for root in ROOT_DIRS:
        for subfolder, prefix in zip(SUBFOLDERS, PREFIXES):
            target = root / subfolder
            if not target.exists() or not target.is_dir():
                print(f"[WARN] folder not found: {target}")
                continue

            print(f"\nProcessing videos in: {target} (prefix='{prefix}')")
            rename_videos_in(target, prefix)

            new_folder = root / prefix
            if new_folder.exists():
                print(f"[SKIP] cannot rename folder '{target.name}' → '{new_folder.name}' (already exists)")
            else:
                print(f"[RENAME FOLDER] {target.name} → {new_folder.name}")
                target.rename(new_folder)


