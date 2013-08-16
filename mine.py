#!/usr/bin/env python
# mine.py
import sys
from toyminer.sync import SyncMiner
from toyminer.jobs import Job

job = Job(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
sys.stdout.write(SyncMiner().mine(job))
