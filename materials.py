#!/usr/bin/python3
# Author: Luis Antonio Obis Aparicio (@lobis)

# usage: running the script (python3 generate_materials.py) will process all files in 'xml_files' sequentially
# and produce a merged file named 'filename' after checking for duplicates (raising exception in that case)

import os
import xml.etree.ElementTree as ET
import json

files_to_generate = {
    "materials.xml": ["NIST.xml", "userDefined/other.xml"],
    "gases.xml": ["NIST.xml", "userDefined/gases.xml"]
}


def validate_and_merge(filename, xml_files):
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
            #assert (material in references), f"'{material}' is not a valid reference, probably not defined before"
            if material not in references:
                continue
            for alias in alias_list:
                assert (
                    alias not in references), f"'{alias}' is not a valid alias, it has been used before"
                references.add(alias)
                for child in materials:
                    if (child.attrib["name"] == material):
                        # we matched the alias, we copy the material and change its name to match our alias
                        alias_attrib = child.attrib.copy()
                        alias_attrib["name"] = alias
                        material_alias = ET.SubElement(
                            alias_elements, child.tag, **alias_attrib)
                        for subchild in child:
                            ET.SubElement(material_alias,
                                          subchild.tag, **subchild.attrib)

    materials.extend(alias_elements)

    try:
        # write pretty
        from xml.dom import minidom

        s = ET.tostring(materials)
        s = minidom.parseString(s).toprettyxml(indent="   ")
        lines = [line for line in s.split('\n') if line.strip()]
        """
        # add custom header using the version file
        with open("version", "r") as f:
            version = f.readlines()[0].strip("\n").strip("\t").strip(" ")
            print(f"increasing version of '{filename}' from '{version}'...")
            version_split = version.split(".")
            # increase minor version number
            version_split[2] = str(int(version_split[2]) + 1)
            version = ".".join(version_split)
            print(f"...to '{version}'")

        #lines[0] = "<?xml version=\"" + version + "\" encoding=\"UTF-8\" ?>"
        """
        lines[0] = ""
        s = "\n".join(lines)
        with open(filename, "w") as f:
            f.write(s + "\n")

    except Exception as e:
        print(e)
        tree = ET.ElementTree(materials)
        tree.write(filename, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":

    for filename, xml_files in files_to_generate.items():
        print(filename, xml_files)
        validate_and_merge(filename, xml_files)

"""
    # increase version file
    with open("version", "r") as f:
        version = f.readlines()[0].strip("\n").strip("\t").strip(" ")
        print(f"increasing version file from '{version}'...")
        version_split = version.split(".")
        # increase minor version number
        version_split[2] = str(int(version_split[2]) + 1)
        version = ".".join(version_split)
        print(f"...to '{version}'")

    with open("version", "w") as fw:
        fw.write(version + "\n")  # update the version tracking file
"""
