#!/usr/bin/python3
# Author: Luis Antonio Obis Aparicio (@lobis)

# usage: running the script (python3 generate_materials.py) will process all files in 'xml_files' sequentially
# and produce a merged file named 'merge_filename' after checking for duplicates (raising exception in that case)

import os
import xml.etree.ElementTree as ET
import json

# order is important! only files in this list will be procesed and combined into `materials.xml`, in the order they appear
xml_files = ["NIST.xml", "gases.xml", "other.xml"]

merge_filename = "materials.xml"

if __name__ == "__main__":
    references = set()
    materials = ET.Element("materials")
    for xml_file in xml_files:
        # assert all files exist
        assert (os.path.isfile(xml_file)
                ), f"'{os.path.abspath(xml_file)}' does not exist"

        tree = ET.parse(xml_file)
        root = tree.getroot()
        for child in root:
            # element, isotope, material...
            for prop in child:
                if ("ref" in prop.attrib.keys()):
                    # check all 'ref' point to references defined before
                    assert prop.attrib["ref"] in references, f"'{prop.attrib['ref']}' not in references, probably not defined before!"
            name = child.attrib["name"]
            if (name in references):
                raise Exception(f"'{name}' is duplicated!")

            references.add(name)
        materials.extend(root)

    # process aliases defined in 'aliases.json'
    alias_elements = ET.Element("root")

    with open('aliases.json') as json_file:
        aliases = json.load(json_file)
        for material, alias_list in aliases.items():
            assert (
                material in references), f"'{material}' is not a valid reference, probably not defined before"
            for alias in alias_list:
                assert (alias not in references), f"'{alias}' is not a valid alias, it has been used before"
                references.add(alias)
                for child in materials:
                    if (child.attrib["name"] == material):
                        # we matched the alias, we copy the material and change its name to match our alias
                        alias_attrib = child.attrib.copy()
                        alias_attrib["name"] = alias
                        material_alias = ET.SubElement(alias_elements, child.tag, **alias_attrib)                        
                        for subchild in child:
                            ET.SubElement(material_alias, subchild.tag, **subchild.attrib)

    materials.extend(alias_elements)

    try:
        # write pretty
        from xml.dom import minidom

        s = ET.tostring(materials)
        s = minidom.parseString(s).toprettyxml(indent="   ")
        s = "\n".join([line for line in s.split('\n') if line.strip()])

        with open(merge_filename, "w") as f:
            f.write(s + "\n")

    except Exception as e:
        print(e)
        tree = ET.ElementTree(materials)
        tree.write(merge_filename, encoding="iso-8859-1",
                   xml_declaration=True, method="xml")
