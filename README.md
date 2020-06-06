# materials

This is a small project to host material definitions to be used in a GDML Geometry simulation inside Geant4.

The contents of this repository will be synchronized with the [following website](https://sultan.unizar.es/materials/).

The main objective is to define material files with version traceability features that will be integrated with restG4 and TRestG4Metadata.
To allow for this traceability we should define a reference string at the beginning of the materials file, 
enclosed in a comment between the following identificative header `##VERSION ##`.

It shoould include a line as the following line.
```
<!-- ##VERSION REST materials 1.0## -->
```

