#!/usr/bin/python3
# Author: Luis Antonio Obis Aparicio (@lobis)

# usage: running the script (python3 generate_materials.py) will process all files in 'xml_files' sequentially 
# and produce a merged file named 'merge_filename' after checking for duplicates (raising exception in that case)

import os
import xml.etree.ElementTree as ET

# order is important! only files in this list will be procesed and combined into `materials.xml`, in the order they appear
xml_files = ["NIST.xml", "gases.xml"]

merge_filename = "materials.notfinal.xml" # do not name it `materials.xml` yet as not all materials all included

if __name__ == "__main__":
    references = set()
    materials = ET.Element("materials")
    for xml_file in xml_files:
        # assert all files exist
        assert (os.path.isfile(xml_file)), f"'{os.path.abspath(xml_file)}' does not exist"

        tree = ET.parse(xml_file)
        root = tree.getroot()
        for child in root:
            # element, isotope, material...
            for prop in child:
                if ("ref" in prop.attrib.keys()):
                    # check all 'ref' point to references defined before
                    assert prop.attrib["ref"] in references, f"'{prop.attrib['ref']}' not in references, probably not defined before!"
            # print(child.tag, child.attrib)
            name = child.attrib["name"]
            if (name in references):
                raise Exception(f"'{name}' is duplicated!")
            
            references.add(name)
        materials.extend(root)

    try:
        # write pretty
        from xml.dom import minidom

        s = ET.tostring(materials)
        s = minidom.parseString(s).toprettyxml(indent="   ")
        s = "\n".join([line for line in s.split('\n') if line.strip()])

        with open(merge_filename, "w") as f:
            f.write(s)
            print(s)

    except Exception as e:
        print(e)
        tree = ET.ElementTree(materials)
        tree.write(merge_filename, encoding="iso-8859-1", xml_declaration=True, method="xml")

