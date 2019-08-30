#! /usr/bin/env python
# coding=utf-8
# Copyright (c) 2019 Florian Trabauer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# This script extracts metadata from scaned deliverynotes. It is designed for
# deliverynotes in A4 from Moneysoft scanned at 200dpi in color or grayscale.
# It scans all jpg images in the current directory, creates two
# folders processed for the successfull renamed images and not-recognized for
# the images that haven't renamed.



import cv2
import pytesseract
import re
from pathlib import Path
import shutil
import os.path
import os

if not os.path.isdir('not-recognized'):
    os.mkdir('not-recognized')
if not os.path.isdir('processed'):
    os.mkdir('processed')

p = Path('.')
files = sorted(p.glob('*.jpg')) + sorted(p.glob('*.JPG'))
for path in files:
    dnImg = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    print('===========\n' + str(path))
    dnNo = ''
    reading = pytesseract.image_to_string(dnImg[587:900, 0:1000], lang='deu')
    print(reading)
    m = re.search(r'Lieferschein\W+([0-9]{7})', reading)
    if m:
        dnNo = m.group(1)
        print(dnNo)
    else:
        print("Dokument nicht erkannt!")
        shutil.move(path, os.path.join('not-recognized', os.path.basename(path)))
        continue
    dateStr = ''
    customerNoStr = ''
    reading = pytesseract.image_to_string(dnImg[371:750, 1000:1580], lang='deu')
    m = re.search(r'Datum:\W+([0-9]{2}\.[0-9]{2}\.[0-9]{4})\W+Kundennr.:\W+([0-9]{6})', reading)
    if m:
        dateStr = m.group(1)
        print(dateStr)
        customerNoStr = m.group(2)
        print(customerNoStr)
    else:
        print("kein Datum gefunden!")
    recipentStr = ''
    reading = pytesseract.image_to_string(dnImg[300:750, 10:800], lang='deu')
    recipentStr = reading.replace('\n', '-').replace(' ', '-')
    print(recipentStr)
    pageIndex = 0
    filename = 'processed/'+dnNo+'-'+dateStr+'-'+customerNoStr+'-'+recipentStr+'-'+str(pageIndex)+'.jpg'
    while os.path.exists(filename):
        pageIndex = pageIndex + 1
        filename = 'processed/'+dnNo+'-'+dateStr+'-'+customerNoStr+'-'+recipentStr+'-'+str(pageIndex)+'.jpg'

    print('moving to '+filename)
    shutil.move(path, filename)
