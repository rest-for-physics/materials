using namespace std;

#include "G4NistManager.hh"
#include <cstdio>

void generateMaterials(const string &outputFilename = "NIST.xml") {

    FILE *pFile;
    pFile = fopen(outputFilename.c_str(), "w");

    auto nistManager = G4NistManager::Instance();

    fprintf(pFile, "<materials>\n");
    fprintf(pFile, "\t\n<!-- periodic table elements -->\n");

    for (const auto &elementName : nistManager->GetNistElementNames()) {
        auto element = nistManager->FindOrBuildElement(elementName, true);
        if (element == nullptr) {
            continue;
        }

        fprintf(pFile, "\t\n<!-- element %s -->\n", element->GetName().c_str());
        for (size_t i = 0; i < element->GetNumberOfIsotopes(); i++) {
            auto isotope = element->GetIsotope(i);
            string isotopeString = "";

            fprintf(pFile, "\t<isotope N=\"%d\" Z=\"%d\" name=\"%s\">\n\t\t<atom type=\"A\" value=\"%f\"/>\n\t</isotope>\n", isotope->GetN(), isotope->GetZ(), isotope->GetName().c_str(), isotope->GetA() / CLHEP::gram);
        }

        fprintf(pFile, "\t<element name=\"%s\">\n", element->GetName().c_str());
        for (size_t i = 0; i < element->GetNumberOfIsotopes(); i++) {
            auto isotope = element->GetIsotope(i);
            fprintf(pFile, "\t\t<fraction n=\"%f\" ref=\"%s\"/>\n", element->GetRelativeAbundanceVector()[i], isotope->GetName().c_str());
        }
        fprintf(pFile, "\t</element>\n");

        if (elementName == "Cf") break;// can't go further
    }

    fprintf(pFile, "\t\n<!-- NIST materials -->\n");

    for (const auto &materialName : nistManager->GetNistMaterialNames()) {
        auto material = nistManager->FindOrBuildMaterial(materialName);
        fprintf(pFile, "\t\n<!-- material %s -->\n", material->GetName().c_str());
        string state = "undefined";
        if (material->GetState() == G4State::kStateGas) {
            state = "gas";
        } else if (material->GetState() == G4State::kStateLiquid) {
            state = "liquid";
        }
        if (material->GetState() == G4State::kStateSolid) {
            state = "solid";
        }

        fprintf(pFile, "\t<material name=\"%s\" state=\"%s\">\n", material->GetName().c_str(), state.c_str());
        fprintf(pFile, "\t\t<D value=\"%.5e\" unit=\"g/cm3\"/>\n", material->GetDensity() / CLHEP::gram * CLHEP::centimeter * CLHEP::centimeter * CLHEP::centimeter);
        for (size_t i = 0; i < material->GetNumberOfElements(); i++) {
            fprintf(pFile, "\t\t<fraction n=\"%f\" ref=\"%s\"/>\n", material->GetFractionVector()[i], material->GetElement(i)->GetName().c_str());
        }
        fprintf(pFile, "\t</material>\n");
    }
    fprintf(pFile, "</materials>\n");
    fclose(pFile);
}

int main() {
    cout << "generating NIST material file" << endl;
    generateMaterials();
}
