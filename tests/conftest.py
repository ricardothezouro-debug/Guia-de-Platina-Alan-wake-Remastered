"""Permite rodar os testes pela raiz do guia ou pela raiz do Sidekick."""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "src"
if str(SOURCE) not in sys.path:
    sys.path.insert(0, str(SOURCE))

# A pasta de dados do Sidekick é dado real do usuário: progresso de platinas,
# marcações, presets. Teste nenhum grava lá, nem quando alguém esquece de
# isolar o APPDATA na linha de comando.
_ISOLATED = tempfile.mkdtemp(prefix="aw-guide-tests-")
for _name in ("APPDATA", "LOCALAPPDATA", "XDG_CONFIG_HOME"):
    os.environ[_name] = _ISOLATED
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
