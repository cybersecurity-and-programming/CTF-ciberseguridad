#!/bin/bash

for f in *; do
    if [ -f "$f" ]; then
        echo -e "\e[32m======== $f\e[0m"
        echo -e "\e[32mFile Name        : $f\e[0m"
        echo -e "\e[32mFile Size        : $(stat -c%s "$f") bytes\e[0m"
        echo -e "\e[32mFile Type        : $(file -b "$f")\e[0m"
        echo -e "\e[32mMIME Type        : $(file --mime-type -b "$f")\e[0m"

        echo -e "\e[32mMD5 Hash         : $(md5sum "$f" | awk '{print $1}')\e[0m"
        echo -e "\e[32mSHA1 Hash        : $(sha1sum "$f" | awk '{print $1}')\e[0m"
        echo -e "\e[32mSHA256 Hash      : $(sha256sum "$f" | awk '{print $1}')\e[0m"

        echo -e "\e[32mCreated          : $(stat -c %w "$f" 2>/dev/null)\e[0m"
        echo -e "\e[32mModified         : $(stat -c %y "$f")\e[0m"
        echo -e "\e[32mAccessed         : $(stat -c %x "$f")\e[0m"

        echo -e "\e[32mEntropy          : $(ent "$f" | grep Entropy | awk '{print $3}')\e[0m"

        # Detect PE
        if file "$f" | grep -q "PE32"; then
            echo -e "\e[32mPE File Detected : Yes\e[0m"
            echo -e "\e[32mPE Sections:\e[0m"
            python3 - <<EOF
import pefile
try:
    pe = pefile.PE("$f")
    for section in pe.sections:
        print("\033[32m -", section.Name.decode().rstrip('\x00'), "Entropy:", section.get_entropy(), "\033[0m")
except:
    print("\033[32mError reading PE structure\033[0m")
EOF
        fi

        # Detect MSI (compatible con Kali usando 7z)
        if file "$f" | grep -q "MSI"; then
            echo -e "\e[32mMSI File Detected : Yes\e[0m"
            echo -e "\e[32mMSI Metadata (via 7z):\e[0m"

            TMPDIR=$(mktemp -d)
            7z x "$f" -o"$TMPDIR" >/dev/null 2>&1

            if [ -f "$TMPDIR/Property" ]; then
                grep -E "ProductName|Manufacturer|ProductVersion|ProductCode" "$TMPDIR/Property" | \
                    sed 's/^/\x1b[32m/;s/$/\x1b[0m/'
            else
                echo -e "\e[32mNo Property table found\e[0m"
            fi

            rm -rf "$TMPDIR"
        fi

        echo
    fi
done

