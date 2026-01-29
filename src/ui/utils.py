# Utility functions for UI components

import re

def clean_string(text):
    return re.sub(r'[^0-9,]', '', text)