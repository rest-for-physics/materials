# materials

This is a small project to host material definitions to be used in a GDML Geometry simulation inside Geant4.

The contents of this repository will be synchronized with the [following website](https://sultan.unizar.es/materials/).

The main objective is to define material files with version traceability features that will be integrated with restG4 and TRestGeant4Metadata.
To allow for this traceability we should define a reference string at the beginning of the materials file, 
enclosed in a comment between the following identificative header `##VERSION ##`.

It should include a line as the following inside the header:

```
<!-- ##VERSION REST materials 1.0## -->
```

Feel free to add new materials, upgrade existing ones, or report any issues found within this materials library at the [REST forum](http://ezpc10.unizar.es).

**⚠ WARNING: REST is under continous development.** This README is offered to you by the REST community. Your HELP is needed to keep this file up to date. You are very welcome to contribute fixing typos, updating information or adding new contributions. See also our [Contribution Guide](https://github.com/rest-for-physics/rest-framework/blob/master/CONTRIBUTING.md).
