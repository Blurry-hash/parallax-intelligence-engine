#!/usr/bin/env python3
"""Read-only local environment preflight. Does not infer browser/API entitlements.

No network access, file modifications, secrets or subprocess execution.
Only reports discoverable local runtimes; permission must be independently proven.
"""
from __future__ import annotations
import argparse, json, shutil, sys, platform

TOOLS=("python","git","ffmpeg","ffprobe","node","npm","docker","gh","blender")

def inspect(commands:tuple[str,...] = TOOLS, which=shutil.which) -> dict:
    return {
        'platform':platform.system(),
        'python':'.'.join(map(str,sys.version_info[:3])),
        'local_executables':{x:bool(which(x)) for x in commands},
        'model_integrations':'unknown — no provider has been contacted',
        'browser_automation':'unknown — local executable inspection cannot establish access',
        'external_spending_authorized':False,
        'private_data_upload_authorized':False,
        'consequential_writes_authorized':False,
        'note':'Executable discovered != functionality/authorization verified. Probe harmlessly before claiming use.',
    }

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.parse_args()
    print(json.dumps(inspect(),indent=2))
