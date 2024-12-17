const scxml = require('@scion-scxml/scxml');  // ou une autre bibliothèque SCXML
const fs = require('fs');

// Chemin relatif vers le fichier SCXML
const scxmlFile = './test.scxml';  // Assurez-vous que ce fichier existe

fs.readFile(scxmlFile, 'utf8', (err, data) => {
    if (err) {
        console.error("Erreur lors de la lecture du fichier SCXML:", err);
        return;
    }

    scxml.pathToModel(data, (err, model) => {
        if (err) {
            console.error("Erreur lors de la conversion SCXML:", err);
            return;
        }

        const stateMachine = new scxml.scion.Statechart(model);
        stateMachine.start();
        console.log('État initial :', stateMachine.getConfiguration());
    });
});
