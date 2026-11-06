"""Execute após analise.py: cenário alternativo, sem sobrescrever o principal."""
from pathlib import Path
import os, subprocess, sys, shutil
root=Path(__file__).resolve().parent
other=root/'experimento_taxa_12k'
(other/'dados').mkdir(parents=True,exist_ok=True)
link=other/'dados'/'raw'
if not link.exists():
    try: link.symlink_to(root/'dados'/'raw',target_is_directory=True)
    except OSError: shutil.copytree(root/'dados'/'raw',link)
env=os.environ.copy();env['CWRU_NORMAL_FS']='12000'
subprocess.run([sys.executable,str(root/'analise.py')],cwd=other,env=env,check=True)
print('Cenário alternativo salvo em',other/'resultados')
