# Materials

This is a small project to host material definitions to be used in a GDML Geometry simulation inside Geant4.

The materials produced by this repository are automatically deployed to GitHub Pages where the different xml files can be accessed, for example, the [materials.xml](https://rest-for-physics.github.io/materials/materials.xml) file can be accessed in [https://rest-for-physics.github.io/materials/materials.xml](https://rest-for-physics.github.io/materials/materials.xml).

## How to update

User should only modify the files in `definitions`. In order to propagate changes into output you need to run the Python script (from the root of the repository):

```bash
python materials.py
```

These files are also automatically synced to [following website](https://sultan.unizar.es/materials/).

The main objective is to define material files with version traceability features that will be integrated with restG4 and `TRestGeant4Metadata`.
To allow for traceability we have implemented versioning of the material files via the `version` xml tag. A more sophisticated versioning system is being worked on (https://github.com/rest-for-physics/materials/issues/3).

```
<?xml version="0.0.2" encoding="UTF-8" ?>
<materials>
  ...
</materials>
```

The XML files at the root of the repository are generated via the `materials.py` python script. All this script does is combine diferent XML files into one, while also checking for possible problems such as duplicate materials or undefined references. For example, in order to generate the `gases.xml` file, the script combines the `NIST.xml` file (this file should be the base for all material files) with the `userDefined/gases.xml` file, as you can see here:

```
files_to_generate = {
    "materials.xml": ["NIST.xml", "userDefined/other.xml"],
    "gases.xml": ["NIST.xml", "userDefined/gases.xml"]
}
```

If you want to add a new materials file, you should add the corresponding XML file to the `userDefined` directory, and then add an additional line to the python dictionary above, that references the files you want to combine into one. The `userDefined` materials file should, whenever possible, be constructed from the materials defined in `NIST.xml`.

The script also supports aliases, defined in the `aliases.json` file:

```
{
    "G4_Cu": ["Copper"],
    "G4_Pb": ["Lead"],
    "G4_Al": ["Aluminium"],
    "G4_Cd": ["Cadmium"],
    "G4_STAINLESS-STEEL": ["Steel", "StainlessSteel"]
}
```

This file tells the script that, for example, we want to create a material named `StainlessSteel` that is an exact copy of the material `G4_STAINLESS-STEEL`. This way we can have copies of materials and the user does not need to worry about tracking them and making sure they stay identical. The aliases file is global, if a material is referenced in the `aliases.json` but does not exist in the final materials XML, then it will just ignore it.

Feel free to add new materials, upgrade existing ones, or report any issues found within this materials library at the [REST forum](http://ezpc10.unizar.es).

**⚠ WARNING: REST is under continous development.** This README is offered to you by the REST community. Your HELP is needed to keep this file up to date. You are very welcome to contribute to REST by fixing typos, updating information or adding new contributions. See also our [Contribution Guide](https://github.com/rest-for-physics/rest-framework/blob/master/CONTRIBUTING.md).
